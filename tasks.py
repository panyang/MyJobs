from datetime import date, timedelta, datetime
from itertools import chain
import logging

from celery import task
from celery.schedules import crontab

from django.conf import settings
from django.template.loader import render_to_string
from django.db.models import Q

from myjobs.models import EmailLog, User
from myprofile.models import SecondaryEmail
from mysearches.models import SavedSearch, SavedSearchDigest
from registration.models import ActivationProfile

logger = logging.getLogger(__name__)


@task(name='tasks.send_search_digests')
def send_search_digests():
    """
    Daily task to send saved searches. If user opted in for a digest, they
    receive it daily and do not get individual saved search emails. Otherwise,
    each active saved search is sent individually.

    Catches and logs any exceptions that occur while sending emails.
    """

    def filter_by_time(qs):
        """
        Filters the provided query set for emails that should be sent today

        Inputs:
        :qs: query set to be filtered

        Outputs:
        :qs: filtered query set containing today's outgoing emails
        """
        today = datetime.today()
        day_of_week = today.isoweekday()

        daily = qs.filter(frequency='D')
        weekly = qs.filter(frequency='W', day_of_week=str(day_of_week))
        monthly = qs.filter(frequency='M', day_of_month=today.day)
        return chain(daily, weekly, monthly)


    log_text = '{exception} - user: {user_id}, {object_type}: {object_id}'

    digest = SavedSearchDigest.objects.filter(is_active=True)
    digest = filter_by_time(digest)
    for obj in digest:
        try:
            obj.send_email()
        except Exception, e:
            logger.error(log_text.format(exception=e,
                                         user_id=obj.user.id,
                                         object_type='saved search digest',
                                         object_id=obj.id))

    not_digest = SavedSearchDigest.objects.filter(is_active=False)
    for item in not_digest:
        saved_searches = item.user.savedsearch_set.filter(is_active=True)
        saved_searches = filter_by_time(saved_searches)
        for search_obj in saved_searches:
            try:
                search_obj.send_email()
            except Exception, e:
                logger.error(log_text.format(exception=e,
                                             user_id=search_obj.user.id,
                                             object_type='saved search',
                                             object_id=search_obj.id))

@task(name='task.delete_inactive_activations')
def delete_inactive_activations():
    """
    Daily task checks if a activation keys are expired and deletes them.
    Disabled users are exempt from this check.
    """
    
    for profile in ActivationProfile.objects.all():
        try:
            if profile.activation_key_expired():
                user = profile.user
                if not user.is_disabled and not user.is_active:
                    user.delete()
                    profile.delete()
        except User.DoesNotExist:
            profile.delete()


@task(name='tasks.process_batch_events')
def process_batch_events():
    """
    Processes all events that have accumulated over the last day, sends emails
    to inactive users, and disables users who have been inactive for a long
    period of time.
    """
    now = date.today()
    EmailLog.objects.filter(received__lte=now-timedelta(days=60),
                            processed=True).delete()
    new_logs = EmailLog.objects.filter(processed=False)
    for log in new_logs:
        user = User.objects.get_email_owner(email=log.email)
        if not user:
            # This can happen if a user removes a secondary address or deletes
            # their account between interacting with an email and the batch
            # process being run
            # There is no course of action but to ignore that event
            continue
        if user.last_response < log.received:
            user.last_response = log.received
            user.save()
        log.processed = True
        log.save()

    # These users have not responded in a month. Send them an email if they
    # own any saved searches
    inactive = User.objects.select_related('savedsearch_set')
    inactive = inactive.filter(Q(last_response=now-timedelta(days=30)) |
                               Q(last_response=now-timedelta(days=36)))

    for user in inactive:
        if user.savedsearch_set.exists():
            time = (now - user.last_response).days
            message = render_to_string('myjobs/email_inactive.html',
                                       {'user': user,
                                        'time': time})
            user.email_user('Account Inactivity', message,
                            settings.DEFAULT_FROM_EMAIL)

    # These users have not responded in a month and a week. Stop sending emails.
    stop_sending = User.objects.filter(
        last_response__lte=now-timedelta(days=37))
    for user in stop_sending:
        user.opt_in_myjobs = False
        user.save()
