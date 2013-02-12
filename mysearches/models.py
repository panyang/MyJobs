from django.db import models


class SavedSearch(models.Model):
    FREQUENCY_CHOICES = (
        ('D', 'Daily'),
        ('W', 'Weekly'),
        ('M', 'Monthly'))

    label = models.CharField(max_length=60, verbose_name="Label")
    url = models.URLField(max_length=300, verbose_name="URL of Search Results")
    feed = models.URLField(max_length=300)
    is_active = models.BooleanField(default=True, verbose_name="Is this agent active?")
    email = models.EmailField(max_length=255, verbose_name="Send results to")
    frequency = models.CharField(max_length=2, choices=FREQUENCY_CHOICES,
                                 default='W', verbose_name="How often do you want an email?")
    delivery_date = models.DateTimeField(blank=True,null=True)
    notes = models.TextField(blank=True,null=True)
    
