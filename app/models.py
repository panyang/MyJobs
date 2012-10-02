from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from social_auth.signals import pre_update
from social_auth.backends.facebook import FacebookBackend
from django.db.models.signals import post_save


class CustomUserManager(models.Manager):
    def create_user(self, username, email):
        """allows creation of users without email address"""
        return self.model._default_manager.create(username=username)


class CustomUser(models.Model):
    """Implements social auth custom user data"""
    username = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)

    objects = CustomUserManager()

    def is_authenticated(self):
        """Always returns true"""
        return True


class UserProfile(models.Model):
    """User profile data for my.jobs site."""
    user = models.OneToOneField(User)
    # Policy Settings
    opt_in_myjobs = models.BooleanField(_('Receive messages from my.jobs'),
        default=True,
        help_text=_('Checking this enables my.jobs\
                     to send email updates to you.'))
    opt_in_dotjobs = models.BooleanField(
        _('Receive messages from dotjobs site owners'), default=True,
        help_text=_('Checking this allows employers who own\
                    .jobs Career Microsites to communicate with you.'))
    enable_public_profile = models.BooleanField(
        _("Activate Public Profile"), default=True,
        help_text=_("Check if you want your public profile to be visible."))    
    # Public Profile Fields
    public_headline = models.CharField(_("Headline"), max_length=255, null=True,
        blank=True, 
        help_text=_("You in on sentence. Shown on your public profile."))
    public_summary = models.TextField(_("Summary"), null=True, blank=True,
        help_text=_("A brief summary. Shown on your public profile."))
    

# Signal Handlers
def facebook_extra_values(sender, user, response, details, **kwargs):
    """Handles extra values from Facebook by ignoring them."""
    return False

pre_update.connect(facebook_extra_values, sender=FacebookBackend)

def create_user_profile(sender, instance, created, **kwargs):
    """Signal Handler for new users. Creates a UserProfile object

    See Django user profile documentation.
    """

    if created:
        UserProfile.objects.create(user=instance)

# Activate Signal Handlers
post_save.connect(create_user_profile, sender=User)
