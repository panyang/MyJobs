from django.db import models
from django.contrib.sites.models import Site
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from basex import BaseX, BaseXError
from django.conf import settings


class Shorty(models.Model):
    """Short url model. Domains are pulled from the django.contrib.sites.

    Short URLs are this models PK encoded in baseX using
    settings.SHORTY_CHARACTER_SET.

    Attributes:

    from_site -- Site responsible for creating the shorty
    from_url -- URL responsible for creating the shorty
    to_url -- the destination URL
    shorty -- the short URL
    redirect_type -- the type of redirect to return
    notes -- user notes
    created -- creation timestamp
    utm_source -- Google analytics source
    utm_medium -- Google analytics medium
    utm_term -- Google analytics search keyword
    utm_content -- Google analytics content
    utm_campaign -- Google analytics campaign
    """

    CHOICES = (
        (_('301 - permanent'), '301'),
        (_('302 - unspecified'), '302'),
        (_('303 - see other'), '303'),
        (_('307 - temporary'), '307'),
        )
    created = models.DateTimeField(_('Created on'), auto_now_add=True)
    from_site = models.ForeignKey(Site, related_name="short_urls")
    from_url = models.URLField(_('Source URL'), max_length=200,
        help_text=_('Must start with _'))
    to_url = models.URLField(_('Destination URL'))
    shorty = models.CharField(_('Encoded IDdbd'), max_length=10,
                              blank=True, null=True, db_index=True)
    shorty_url = models.URLField(_('Short URL'),
                                 db_index=True)
    redirect_type = models.CharField(_('Redirect Type'),
                                     max_length=3,
                                     choices=CHOICES,
                                     default='301')
    notes = models.TextField(_('Notes'), null=True, blank=True)
    created = models.DateTimeField(_('Created Date and Time'),
                                   auto_now_add=True)
    # see Google's URL builder for details on UTM Parameters:
    # http://www.google.com/support/analytics/bin/answer.py?answer=55578    
    utm_source = models.CharField(_('Analytics source'),
                                  max_length=80,
                                  null=True,
                                  blank=True,
                                  default='myjobs')
    utm_medium = models.CharField(_('Analytics medium'), max_length=80,
        null=True, blank=True, default=_('social'),
        help_text=_('Media for this campaign (cpc, email, social)'))
    utm_term = models.CharField(_('Analytics term'), max_length=120, null=True,
        blank=True, help_text=_('Keyword for this URL'))
    utm_content = models.CharField(_('Analytics Content'), max_length=80,
        null=True, blank=True,
        help_text=_('Use to differentiate links that point to the same URL'))
    utm_campaign = models.CharField(_('Analytics Content'), max_length=80,
        null=True, blank=True,
        help_text=_('Use to differentiate links that point to the same URL'),
        default='myjobs')
    
    def shorty(self):
        """Returns encoded value for shorty"""
        if self.pk is not '':
            s = BaseX(self.pk, settings.SHORTY_CHARACTER_SET)
        else:
            raise BaseXError(_('Save shorty model before accessing short url'))
        return s.__str__()
        # TODO: Need to add some logic to deal with avoiding collisions
        # with existing URLS.py

    def save(self):
        """Custom save method that saves short URL to database on save()"""
        # standard presave, super, post save pattern
        # save the model and let the db create the primary key
        super(Shorty, self).save()
        # then encode the URL
        s = Shorty(number=self.pk.__int__(),
                    character_set=settings.SHORTY_CHARACTER_SET)
        self.shorty = (s.__str__())
        # finally, save the model, this time with the short URL.
        super(Shorty, self).save()

    def __unicode__(self):
        return u'%s -> %s' % self.shorty_url, self.to_url

    
class Click(models.Model):
    """Stores click history"""
    site = models.ForeignKey(Site, null=True, blank=True)
    # We can have anonymous users, so there may be no relationship here
    user = models.ForeignKey(User, null=True, related_name="short_url_history")
    visitor = models.ForeignKey(User, blank=True, null=True)
    destination_url = models.URLField(_('Destination  URL'), max_length=200,
        help_text=_('Destination at the time the link was clicked'))
    destination_domain = models.CharField(_('Destination Domain'), max_length=200,
        help_text=_('Destination Domain at the time the link was clicked'))
    created = models.DateTimeField(_('Date & Time'), auto_now_add=True)
    # Optional Referrer Info (it is impossible to know the unknowable)
    referrer_url = models.URLField(_('Referring URL'), max_length=200,
                                   null=True, blank=True)
    referrer_domain = models.CharField(_('Referring Domain'), max_length=200,
                                       null=True, blank=True)

    class Meta:
        ordering = ['-created']
        verbose_name = _('Short URL History')
