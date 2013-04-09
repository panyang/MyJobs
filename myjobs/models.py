import datetime
import urllib, hashlib

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, _user_has_perm
from django.core.mail import send_mail
from django.db import models
from django.db.models.signals import post_save
from django.utils.translation import ugettext_lazy as _

from default_settings import GRAVATAR_URL_PREFIX, GRAVATAR_URL_DEFAULT
from registration import signals as custom_signals

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
        user.gravatar = user.email
        user.save(using=self._db)

        custom_signals.email_created.send(sender=self,user=user,
                                          email=email)
        if send_email:
            custom_signals.send_activation.send(sender=self,user=user,
                                                email=email)
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
        user.gravatar = user.email
        user.set_password(password)
        user.save(using=self._db)
        return user
        
    def create_superuser(self, **kwargs):
        email = kwargs['email']
        password = kwargs['password']
        if not email:
            raise ValueError('Email address required.')
        u = self.model(email=CustomUserManager.normalize_email(email))
        u.is_staff = True
        u.is_active = True
        u.is_superuser = True
        u.gravatar = u.email
        u.set_password(password)
        u.save(using=self._db)
        return u

    def not_disabled(self, user):
        """
        Used by the user_passes_test decorator to set view permissions
        """
        
        return not user.is_disabled

    def is_active(self, user):
        """
        Used by the user_passes_test decorator to set view permissions
        """

        return user.is_active

# New in Django 1.5. This is now the default auth user table. 
class User(AbstractBaseUser):
    email = models.EmailField(verbose_name=_("email address"),
                              max_length=255, unique=True, db_index=True)
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)
    gravatar = models.EmailField(verbose_name=_("gravatar email"),
                                 max_length=255, db_index=True, blank=True,
                                 null=True)

    # Permission Levels
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
    is_disabled = models.BooleanField(_('disabled'), default=False)

    # Communication Settings
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

    def has_perm(self, perm, obj=None):
        """
        Returns True if the user has the specified permission. This method
        queries all available auth backends, but returns immediately if any
        backend returns True. Thus, a user who has permission from a single
        auth backend is assumed to have permission in general. If an object is
        provided, permissions for this specific object are checked.
        """

        # Active superusers have all permissions.
        if self.is_active and self.is_superuser:
            return True

        # Otherwise we need to check the backends.
        return _user_has_perm(self, perm, obj)

    def has_perms(self, perm_list, obj=None):
        """
        Returns True if the user has each of the specified permissions. If
        object is passed, it checks if the user has all required perms for this
        object.
        """
        for perm in perm_list:
            if not self.has_perm(perm, obj):
                return False
        return True

    def has_module_perms(self, app_label):
        """
        Returns True if the user has any permissions in the given app label.
        Uses pretty much the same logic as has_perm, above.
        """
        # Active superusers have all permissions.
        if self.is_active and self.is_superuser:
            return True

        return _user_has_module_perms(self, app_label)

    def get_username(self):
        return self.email

    def get_short_name(self):
        return self.email

    def get_gravatar_url(self, size=20):
        gravatar_url = GRAVATAR_URL_PREFIX + hashlib.md5(self.gravatar.lower()).hexdigest() + "?"
        gravatar_url += urllib.urlencode({'d':GRAVATAR_URL_DEFAULT,
                                          's':str(size)})
        return gravatar_url

    def disable(self):
        self.is_active = False
        self.is_disabled = True
        self.save()
        
        custom_signals.user_disabled.send(sender=self, user=self,
                                          email=self.email)

