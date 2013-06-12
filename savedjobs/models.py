from django.db import models
from django.utils import timezone

class SavedJob(models.Model):
    """
    Defines user-specific saved job information.
    
    """
    user = models.ForeignKey('myjobs.User', db_index=True)
    date_saved = models.DateTimeField('Date Saved', default=timezone.now)
    url = models.URLField(blank=True, null=True)
    uid = models.IntegerField(db_index=True, unique=True, blank=True, null=True)
    title = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    city = models.CharField(max_length=200, blank=True, null=True)
    state = models.CharField(max_length=200, blank=True, null=True)
    country = models.CharField(max_length=200, blank=True, null=True)
    onet = models.CharField(max_length=10, blank=True, null=True)
    from_microsite = models.BooleanField(default=False)
    
    def __unicode__(self):
        return "%s-%s" % (self.user.email, self.title)

    class Meta:
        verbose_name = "Saved Job"
        verbose_name_plural = "Saved Jobs"
