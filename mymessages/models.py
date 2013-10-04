import datetime

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import Group

from myjobs.models import User


def start_default():
    return datetime.datetime.now()


def expire_default():
    return datetime.datetime.now() + datetime.timedelta(days=14)


class Message(models.Model):
    """
    Message
    """
    TYPE_OF_MESSAGES = (
        ('error', 'Error'),
        ('info', 'Info'),
        ('block', 'Notice'),
        ('success', 'Success'),
    )
    group = models.ManyToManyField(Group)
    users = models.ManyToManyField(User, through='MessageInfo')
    subject = models.CharField("Subject", max_length=200)
    message_type = models.CharField("Type of message", choices=TYPE_OF_MESSAGES,
                                    max_length=200)
    body = models.TextField('Body')
    start_on = models.DateTimeField('start on', default=start_default)
    expire_at = models.DateTimeField('expire at',
                                     default=expire_default,
                                     null=True,
                                     help_text="Default is two weeks " +
                                               "after message is sent.")
    btn_text = models.CharField('Button Text', max_length=100, default='Okay')

    def __unicode__(self):
        return self.subject


class MessageInfo(models.Model):
    """
    Through model for Message.
    """
    user = models.ForeignKey(User)
    message = models.ForeignKey(Message)
    read = models.BooleanField(default=False, db_index=True)
    read_at = models.DateTimeField('read at', null=True)
    expired = models.BooleanField(default=False, db_index=True)
    expired_on = models.DateTimeField('expired on', null=True)

    def __unicode__(self):
        return self.message.subject

    def is_unread(self):
        return bool(self.read_at is None)

    def mark_unread(self):
        self.read = False
        self.read_at = None
        self.save()

    def mark_read(self):
        self.read = True
        self.read_at = datetime.datetime.now()
        self.save()

    def mark_expired(self):
        self.read = False
        self.expired = True
        self.expired_on = datetime.datetime.now()
        self.save()

    def expired_time(self):
        message = self.message
        now = timezone.now()
        if timezone.is_naive(self.message.expire_at):
            message.expire_at = timezone.make_aware(
                message.expire_at, timezone.UTC())
        if timezone.is_naive(self.message.start_on):
            message.start_on = timezone.make_aware(
                message.start_on, timezone.UTC())
        date_expired = (message.expire_at - message.start_on) + \
                       message.start_on
        if now > date_expired:
            self.mark_expired()
            return True
        else:
            return False


def get_messages(user):
    """
    Gathers all Messages. Checks when they start, expire against current time.

    Inputs:
    :user:              User obj to get user's groups

    Outputs:
    :active_messages:   A list of messages that starts before the current
                        time and expires after the current time. 'active'
                        messages.
    """
    now = timezone.now()
    groups = Group.objects.filter(user=user)
    messages = set(Message.objects.filter(group__in=groups, expire_at__gt=now))
    active_messages = []
    for message in messages:
        if message.start_on < now < message.expire_at:
            active_messages.append(message)
    return active_messages