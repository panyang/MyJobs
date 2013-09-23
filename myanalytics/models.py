import unicodedata

from django.db import models


class SiteViewer(models.Model):
    """
    One individual user of a microsite

    A given user may have multiple aguids, one per device, with a new aguid
    being generated if cookies are disabled/cleared.
    """
    aguid = models.CharField(max_length=36,
                             help_text="Anonymous UUID for the user")
    user  = models.ForeignKey('myjobs.User', blank=True, null=True,
                                    help_text="User's MyJobs account, "
                                              "if one exists")
    view_count = models.IntegerField(default=0, blank=True,
                                     help_text="Number of views for this user")


class SiteView(models.Model):
    """
    Analytics data for a given site view
    """
    ip = models.GenericIPAddressField(help_text="User's IP address")
    viewed = models.DateTimeField(help_text="Date/time that a view took place")
    site_url = models.TextField(help_text="URL of a given view")
    search_parameters = models.TextField(blank=True,
                                         help_text="Search parameters, if "
                                                   "any, that were used")
    source_codes = models.CharField(max_length=300, blank=True)
    view_source = models.IntegerField(blank=True, null=True)
    goal = models.CharField(max_length=11, blank=True,
                            help_text="Any special events that took place "
                                      "(e.g. saving a search, clicking apply)")
    goal_url = models.TextField(blank=True,
                                help_text="A URL related to the above goal "
                                          "(e.g. a specific job url)")

    # 32767x32767 ought to be enough for anybody
    resolution_w = models.PositiveSmallIntegerField(
        help_text="The user's horizontal resolution")
    resolution_h = models.PositiveSmallIntegerField(
        help_text="The user's vertical resolution")

    viewer = models.ForeignKey('myanalytics.SiteViewer')
    user_agent = models.ForeignKey('myanalytics.UserAgent')

    def save(self, *args, **kwargs):
        self.site_url = unicodedata.normalize('NFKC', self.site_url)
        self.search_parameters = unicodedata.normalize('NFKC',
                                                       self.search_parameters)
        self.source_codes = unicodedata.normalize('NFKC', self.source_codes)
        super(SiteView, self).save(*args, **kwargs)


class UserAgent(models.Model):
    """
    The user agent string for a number of users

    This can be quite lengthy and may not be identifying, so it is separate
    from SiteView and SiteViewer to save some space.
    """
    user_agent = models.TextField(help_text="One entire user agent string")

    def save(self, *args, **kwargs):
        self.user_agent = unicodedata.normalize('NFKC', self.user_agent)
        super(UserAgent, self).save(*args, **kwargs)