from datetime import datetime

from django.conf import settings
from django.db import models
from django.core.mail import send_mail,EmailMultiAlternatives,EmailMessage
from django.template.loader import render_to_string
from mysearches.helpers import parse_rss

class SavedSearch(models.Model):
    FREQUENCY_CHOICES = (
        ('D', 'Daily'),
        ('W', 'Weekly'),
        ('M', 'Monthly'))

    DOM_CHOICES = [(i,i) for i in range(1,31)]
    DOW_CHOICES = (('1', 'Monday'),
                   ('2', 'Tuesday'),
                   ('3', 'Wednesday'),
                   ('4', 'Thursday'),
                   ('5', 'Friday'),
                   ('6', 'Saturday'),
                   ('7', 'Sunday'))

    user = models.ForeignKey('myjobs.User',editable=False)
    url = models.URLField(max_length=300, verbose_name="URL of Search Results")
    label = models.CharField(max_length=60, verbose_name="Label")
    feed = models.URLField(max_length=300)
    is_active = models.BooleanField(default=True, verbose_name="Is this agent active?")
    email = models.EmailField(max_length=255, verbose_name="Send results to")
    frequency = models.CharField(max_length=2, choices=FREQUENCY_CHOICES,
                                 default='W',
                                 verbose_name="How often do you want an email?")
    day_of_month = models.IntegerField(choices=DOM_CHOICES,
                                       blank=True, null=True,
                                       verbose_name="On what day of the month?")
    day_of_week = models.CharField(max_length=2, choices=DOW_CHOICES,
                                   blank=True, null=True,
                                   verbose_name="On what day of the week?")
    notes = models.TextField(blank=True,null=True)
    last_sent = models.DateTimeField(blank=True, null=True,editable=False)

    def get_verbose_frequency(self):
        for choice  in self.FREQUENCY_CHOICES:
            if choice[0] == self.frequency:
                return choice[1]

    def get_verbose_dow(self):
        for choice in self.DOW_CHOICES:
            if choice[0] == self.day_of_week:
                return choice[1]

    def get_feed_items(self, num_items=5):
        return parse_rss(self.feed, self.frequency, num_items=num_items)

    def send_email(self):
        context_dict = {'saved_searches': [self]}
        subject = self.label.strip()
        message = render_to_string('mysearches/email_digest.html',
                                   context_dict)
        msg = EmailMessage(subject, message, settings.DEFAULT_FROM_EMAIL, [self.email])
        msg.content_subtype='html'
        msg.send()
        self.last_sent = datetime.now()
        self.save()

    def save(self, *args,**kwargs):
        if not SavedSearchDigest.objects.filter(user=self.user):
            SavedSearchDigest.objects.create(user=self.user, email=self.email)
        super(SavedSearch,self).save(*args,**kwargs)


class SavedSearchDigest(models.Model):
    is_active = models.BooleanField(default=False,
                                    verbose_name="Would you like to receive all your"
                                    " saved searches as one email?")
    user = models.OneToOneField('myjobs.User', editable=False)
    email = models.EmailField(max_length=255, verbose_name="Send results to")
    
    def send_email(self):
        saved_searches = self.user.savedsearch_set.all()
        subject = 'Your Daily Saved Search Digest'
        context_dict = {'saved_searches': saved_searches}
        message = render_to_string('mysearches/email_digest.html',
                                   context_dict)
        msg = EmailMessage(subject, message, settings.DEFAULT_FROM_EMAIL, [self.email])
        msg.content_subtype='html'
        msg.send()
