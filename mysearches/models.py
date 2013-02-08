from django.db import models


class SavedSearch(models.Model):
    FREQUENCY_CHOICES = (
        ('D', 'Daily'),
        ('W', 'Weekly'),
        ('M'. 'Monthly'))
    
    feed = models.URLField(max_length=300)
    label = models.CharField(max_length=60)
    active = models.BooleanField(default=True)
    canonical_site = models.URLField(max_length=255, blank=True, null=True)
    destination = models.EmailField(max_length=255)
    notes = models.TextField(blank=True,null=True)
    frequency = models.CharField(max_length=2, choices=FREQUENCY_CHOICES,
                                 default='W')
    delivery_date = model.DateTimeField(blank=True,null=True)
    
