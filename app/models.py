import datetime

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.mail import send_mail
from django.utils.translation import ugettext_lazy as _
from social_auth.signals import pre_update
from social_auth.backends.facebook import FacebookBackend
from django.db.models.signals import post_save
from registration.models import *

class CustomUserManager(BaseUserManager):
    def create_inactive_user(self, send_email=True, **kwargs):
        """
        Creates an inactive user, calls the regisration app to generate a
        key and sends an activation email to the user.

        Inputs:
        :send_email: Boolean defaulted to true to signal that an email needs to
        be sent.
        :kwargs: Email and password information

        Outputs:
        :user: User object instance
        """
        email = kwargs['email']
        password = kwargs['password1']
        if not email:
            raise ValueError('Email address required.')
        user = self.model(email=CustomUserManager.normalize_email(email))
        user.set_password(password)
        user.is_active = False
        user.save(using=self._db)

        # Generate and send activation information
        activation_profile = ActivationProfile.objects.generate_key(user)
        if send_email:
            activation_profile.send_activation_email()
        return user
        
    def create_user(self, **kwargs):
        """
        Creates an already activated user.

        """
        email = kwargs['email']
        password = kwargs['password1']
        if not email:
            raise ValueError('Email address required.')
        user = self.model(email=CustomUserManager.normalize_email(email))
        user.is_active = True
        user.set_password(password)
        user.save(using=self._db)
        return user
        
    def create_superuser(self, **kwargs):
        email = kwargs['email']
        password = kwargs['password1']
        if not email:
            raise ValueError('Email address required.')
        u = self.model(email=CustomUserManager.normalize_email(email))
        u.is_staff = True
        u.is_active = True
        u.is_superuser = True
        u.set_password(password)
        u.save(using=self._db)
        return u

# New in Django 1.5. This is now the default auth user table. 
class User(AbstractBaseUser):
    email = models.EmailField(verbose_name="email address",
                              max_length=255, unique=True, db_index=True)
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    is_staff = models.BooleanField(_('staff status'), default=False,
                                   help_text=_("Designates whether the user can " +\
                                               "log into this admin site."))
    is_active = models.BooleanField(_('active'), default=True,
                                    help_text=_("Designates whether this user " +\
                                                "should be treated as active. " +\
                                                "Unselect this instead of deleting accounts."))
    is_superuser = models.BooleanField(_('superuser status'), default=False,
                                       help_text=_("Designates that this user " +\
                                                   "has all permissions without " +\
                                                   "explicitly assigning them."))
    date_joined = models.DateTimeField(_('date joined'),
                                       default=datetime.datetime.now)

    # Policy Settings
    opt_in_myjobs = models.BooleanField(_('Receive messages from my.jobs'),
                                        default=True,
                                        help_text=_('Checking this enables my.jobs\
                                                    to send email updates to you.'))
    
    USERNAME_FIELD = 'email'
    objects = CustomUserManager()

    def __unicode__(self):
        return self.email

    def email_user(self, subject, message, from_email):
        send_mail(subject, message, from_email, [self.email])

# Signal Handlers
def facebook_extra_values(sender, user, response, details, **kwargs):
    """Handles extra values from Facebook by ignoring them."""
    return False
pre_update.connect(facebook_extra_values, sender=FacebookBackend)
