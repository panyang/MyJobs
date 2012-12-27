import datetime

from django.db import models

from myjobs.models import *
from registration.models import *

"""
The terms used in this model abide by the following definitions:

Profile - A module, such as an education profile or an employment history profile,
that contains user data on that particular topic. A user can have multiple instances
of a profile (e.g. a user can have multiple different jobs in their job history).
All Profiles subclass from the BaseProfile abstract class.

ProfileSet - A collection of profiles, such as a resume or a public profile. There
is a many to many relationship between ProfileSets and Profiles. 

ProfileMeta - Through table that defines the relationship meta data between Profiles
and ProfileSets. All ProfileMeta classes subclass from the BaseProfileMeta class.


ATTENTION!
Adding a new profile requires the following things:
1.) The profile class in the format of _type_Profile
2.) A corresponding _type_ProfileMeta class that contains a foreign key to the
    profile and a foreign key to ProfileSet
3.) A many to many field in ProfileSet that links to the profile and has through
set to the meta class.

"""

class ProfileSet(models.Model):
    name = models.CharField(max_length=30)
    user = models.ForeignKey(User)
    name_profiles = models.ManyToManyField('NameProfile', through='NameProfileMeta')
    email_profiles = models.ManyToManyField('EmailProfile', through='EmailProfileMeta')

    def __unicode__(self):
        return self.name

        
# Abstract Base Classes
class BaseProfileMeta(models.Model):
    display_order = models.IntegerField(blank=True)
    display_flag = models.BooleanField(default=True)
    
    class Meta:
        abstract = True


class BaseProfile(models.Model):
    date_created = models.DateTimeField(default=datetime.datetime.now)
    date_updated = models.DateTimeField(default=datetime.datetime.now)

    class Meta:
        abstract = True
        ordering = ['-date_updated']


# Profiles
class NameProfile(BaseProfile):
    user = models.ForeignKey(User)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    primary = models.BooleanField(default=False)

    def __unicode__(self):
        return get_full_name()
        
    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

        
class EmailProfile(BaseProfile):
    user = models.ForeignKey(User)
    email = models.EmailField(max_length=255, blank=True)
    label = models.CharField(max_length=30, blank=True)
    verified = models.BooleanField(default=False)
    verified_date = models.DateTimeField(blank=True)

    def __unicode__(self):
        return self.email

    def send_verification(self):
        """
        Generate a registration key and send a notification to the appropriate
        email. On clicking the link in the activation email, the view sets the
        verified field to true and updates the verified date.
        
        """
        activation = ActivationProfile.objects.generate_key(self.user, self.email)
        activation.send_activation_email()


# Through Tables
class NameProfileMeta(BaseProfileMeta):
    name = models.ForeignKey(NameProfile)
    profile_set = models.ForeignKey(ProfileSet)


class EmailProfileMeta(BaseProfileMeta):
    email = models.ForeignKey(EmailProfile)
    profile_set = models.ForeignKey(ProfileSet)
