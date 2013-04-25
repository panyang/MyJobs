from datetime import date, timedelta
from itertools import chain 

from celery import task
from celery.schedules import crontab

from django.conf import settings
from django.template.loader import render_to_string

from myjobs.models import EmailLog, User
from myprofile.models import SecondaryEmail
from mysearches.models import SavedSearch, SavedSearchDigest

@task(name='tasks.send_search_digests')
def send_search_digests():
    today = datetime.today()
    day_of_week = today.isoweekday()

    digest = SavedSearchDigest.objects.filter(is_active=True)
    for obj in digest:
        obj.send_email()

    not_digest = SavedSearchDigest.objects.filter(is_active=False)    
    for item in not_digest:
        saved_searches = item.user.savedsearch_set.all()
        daily = saved_searches.filter(frequency='D')
        weekly = saved_searches.filter(day_of_week=str(day_of_week))
        monthly = saved_searches.filter(day_of_month=today.day)

        saved_search_objs = chain(daily, weekly, monthly)
        for search_obj in saved_search_objs:
            search_obj.send_email()

@task(name='tasks.process_batch_events')
def process_batch_events():
    now = date.today()
    EmailLog.objects.filter(received__lte=now-timedelta(days=60), processed=True).delete()
    new_logs = EmailLog.objects.filter(processed=False)
    for log in new_logs:
        try:
            # Check if this is a user's primary address
            user = User.objects.get(email=log.email)
        except User.DoesNotExist:
            # It wasn't a primary address; check secondary addresses
            user = SecondaryEmail.objects.get(email=log.email).user
        except SecondaryEmail.DoesNotExist:
            # This can happen if a user removes a secondary address between
            # interacting with an email and the batch process being run
            # There is no course of action but to ignore that event
            continue
        finally:
            log.processed = True
            log.save()
        user.last_response = log.received
        user.save()

    # These users have not responded in a month. Send them an email.
    not_responding = User.objects.filter(last_response=now-timedelta(days=30))
    for user in not_responding:
        message = render_to_string('myjobs/email_inactive.html')
        user.email_user('Account Inactivity', message, settings.DEFAULT_FROM_EMAIL)

    # These users have not responded in a month and a week. Stop sending email.
    stop_sending = User.objects.filter(last_response__lte=now-timedelta(days=37))
    for user in stop_sending:
        user.opt_in_myjobs = False
        user.save()
