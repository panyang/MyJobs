import datetime

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils.translation import ugettext_lazy as _
from social_auth.signals import pre_update
from social_auth.backends.facebook import FacebookBackend
from django.db.models.signals import post_save

class CustomUserManager(BaseUserManager):
    def create_inactive_user(self, **kwargs):
        email = kwargs['email']
        password = kwargs['password1']
        if not email:
            raise ValueError('Email address required.')
        user = self.model(email=CustomUserManager.normalize_email(email))
        user.set_password(password)
        user.is_active = False
        user.save(using=self._db)
        return user
        
    def create_user(self, **kwargs):
        email = kwargs['email']
        password = kwargs['password1']
        if not email:
            raise ValueError('Email address required.')
        user = self.model(email=CustomUserManager.normalize_email(email))
        user.set_password(password)
        user.save(using=self._db)
        return user
        
    def create_superuser(self,email, password):
        u = self.create_user(email, password)
        u.is_staff = True
        u.is_active = True
        u.is_superuser = True
        u.save(using=self._db)
        return u



class User(AbstractBaseUser):
    email = models.EmailField(verbose_name="email address",
                              max_length=255, unique=True, db_index=True)
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    is_staff = models.BooleanField(_('staff status'), default=False, help_text=_("Designates whether the user can log into this admin site."))
    is_active = models.BooleanField(_('active'), default=True, help_text=_("Designates whether this user should be treated as active. Unselect this instead of deleting accounts."))
    is_superuser = models.BooleanField(_('superuser status'), default=False, help_text=_("Designates that this user has all permissions without explicitly assigning them."))
    date_joined = models.DateTimeField(_('date joined'), default=datetime.datetime.now)

    USERNAME_FIELD = 'email'
    objects = CustomUserManager()

    def __unicode__(self):
        return self.email        


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
