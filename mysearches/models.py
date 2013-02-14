from django.db import models


class SavedSearch(models.Model):
    FREQUENCY_CHOICES = (
        ('D', 'Daily'),
        ('W', 'Weekly'),
        ('M', 'Monthly'))

    DOM_CHOICES = [(i,i) for i in range(1,31)]
    DOW_CHOICES = (('Mo', 'Monday'),
                   ('Tu', 'Tuesday'),
                   ('We', 'Wednesday'),
                   ('Th', 'Thursday'),
                   ('Fr', 'Friday'),
                   ('Sa', 'Saturday'),
                   ('Su', 'Sunday'))

    user = models.ForeignKey('myjobs.User',editable=False)
    url = models.URLField(max_length=300, verbose_name="URL of Search Results")
    label = models.CharField(max_length=60, verbose_name="Label")
    feed = models.URLField(max_length=300)
    is_active = models.BooleanField(default=True, verbose_name="Is this agent active?")
    email = models.EmailField(max_length=255, verbose_name="Send results to")
    frequency = models.CharField(max_length=2, choices=FREQUENCY_CHOICES,
                                 default='W',
                                 verbose_name="How often do you want an email?")
    day_of_month = models.IntegerField(choices=DOM_CHOICES, default=1,
                                       blank=True, null=True,
                                       verbose_name="On what day of the month?")
    day_of_week = models.CharField(max_length=2, choices=DOW_CHOICES,
                                   default='Mo', blank=True, null=True,
                                   verbose_name="On what day of the week?")
    notes = models.TextField(blank=True,null=True)
