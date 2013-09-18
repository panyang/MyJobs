import unicodedata

from django.db import models


class SiteViewer(models.Model):
    aguid = models.CharField(max_length=32)
    myjobs_id = models.IntegerField(blank=True, null=True)


class SiteView(models.Model):
    ip = models.GenericIPAddressField()
    viewed = models.DateTimeField()
    site_url = models.CharField(max_length=255)
    search_parameters = models.CharField(max_length=255, blank=True)
    source_codes = models.CharField(max_length=300, blank=True)
    view_source = models.IntegerField(blank=True, null=True)

    # 32767x32767 ought to be enough for anybody
    resolution_w = models.PositiveSmallIntegerField()
    resolution_h = models.PositiveSmallIntegerField()

    viewer = models.ForeignKey('myanalytics.SiteViewer')
    user_agent = models.ForeignKey('myanalytics.UserAgent')

    def save(self, *args, **kwargs):
        self.site_url = unicodedata.normalize('NFKC', self.site_url)
        self.search_parameters = unicodedata.normalize('NFKC',
                                                       self.search_parameters)
        self.source_codes = unicodedata.normalize('NFKC', self.source_codes)
        super(SiteView, self).save(*args, **kwargs)


class UserAgent(models.Model):
    user_agent = models.TextField()

    def save(self, *args, **kwargs):
        self.user_agent = unicodedata.normalize('NFKC', self.user_agent)
        super(UserAgent, self).save(*args, **kwargs)