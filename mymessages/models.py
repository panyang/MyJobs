import datetime

from django.db import models
from django.utils import timezone

from myjobs.models import User


def expire_default():
    return datetime.datetime.now() + datetime.timedelta(days=14)


class Message(models.Model):
    """
    Message
    """
    user = models.ForeignKey(User)
    subject = models.CharField("Subject", max_length=200)
    body = models.TextField('Body')
    sent_at = models.DateTimeField('sent at')
    read = models.BooleanField(default=False, db_index=True)
    read_at = models.DateTimeField('read at', null=True)
    expire_at = models.DateTimeField('expire at',
                                     default=expire_default,
                                     null=True,
                                     help_text="Default is two weeks " +
                                               "after message is sent.")
    expired = models.BooleanField(default=False, db_index=True)
    expired_on = models.DateTimeField('expired on', null=True)

    def __unicode__(self):
        return self.subject

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

    def send_message(self, user):
        self.user = user
        self.save()

    def mark_expired(self):
        self.read = False
        self.expired = True
        self.expired_at = datetime.datetime.now()
        self.save()

    def expired_time(self):
        now = timezone.now()
        if timezone.is_naive(self.expire_at):
            self.expire_at = timezone.make_aware(self.expire_at,
                                                 timezone.UTC())
        date_expired = (self.expire_at - self.sent_at) + self.sent_at
        if now > date_expired:
            self.mark_expired()
            self.save()
            return True
        else:
            return False
