import datetime

from django.contrib.contenttypes.models import ContentType
from django.db import models

from myjobs.models import *
from registration.models import *


class ProfileUnits(models.Model):
    """
    This is the parent class for all user information. Creating any new
    profile unit instances (Education, Name, Email etc) end up in the
    ProfileUnits queryset as well.
    
    """
    date_created = models.DateTimeField(default=datetime.datetime.now)
    date_updated = models.DateTimeField(default=datetime.datetime.now)
    content_type = models.ForeignKey(ContentType, editable=False,null=True)
    user = models.ForeignKey(User)

    def save(self, *args, **kwargs):
        """
        Custom save method to set the content type of the instance.
        
        """
        if(not self.content_type):
            self.content_type = ContentType.objects.get_for_model(self.__class__)
            super(ProfileUnits, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.content_type.name


class Education(ProfileUnits):
    EDUCATION_LEVEL_CHOICES = ( 
        (3, 'High School'),
        (5, 'Associate'),
        (6, 'Bachelor'),
        (7, 'Master'),
        (8, 'Doctoral'),
    )
    organization_name = models.CharField(max_length=255)
    degree_date = models.DateField()
    city_name = models.CharField(max_length=255, blank=True)
    # ISO 3166-2:2007
    country_sub_division_code = models.CharField(max_length=5, blank=True,
                        verbose_name="state") 
    country_code = models.CharField(max_length=3, blank=True,
                        verbose_name="country") # ISO 3166-1
    # ISCED-2011 Can be [0-8]
    education_level_code = models.IntegerField(choices=EDUCATION_LEVEL_CHOICES,
                        verbose_name="education level")
    start_date = models.DateField(blank=True)
    end_date = models.DateField(blank=True)
    education_score = models.CharField(max_length=255, blank=True,
                        verbose_name="GPA")
    degree_name = models.CharField(max_length=255, blank=True)
    degree_major = models.CharField(max_length=255, blank=True)
    degree_minor = models.CharField(max_length=255, blank=True)


class EmploymentHistory(ProfileUnits):
    position_title = models.CharField(max_length=255)
    organization_name = models.CharField(max_length=255)
    start_date = models.DateField()
    current_indicator = models.BooleanField(default=False)

    # Optional fields
    end_date = models.DateField(blank=True)
    city_name = models.CharField(max_length=255, blank=True)
    country_sub_division_code = models.CharField(max_length=5, blank=True) 
    country_code = models.CharField(max_length=3, blank=True)
    description = models.TextField(blank=True)

    # Hidden fields
    industry_code = models.CharField(max_length=255, blank=True)
    job_category_code = models.CharField(max_length=255, blank=True)
    onet_code = models.CharField(max_length=255, blank=True)
        

class Name(ProfileUnits):
    given_name = models.CharField(max_length=30, blank=True)
    family_name = models.CharField(max_length=30, blank=True)
    display_name = models.CharField(max_length=60, blank=True)
    primary = models.BooleanField(default=False)
        
    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def __unicode__(self):
        return self.get_full_name()

        
class SecondaryEmail(ProfileUnits):
    email = models.EmailField(max_length=255, blank=True)
    label = models.CharField(max_length=30, blank=True)
    verified = models.BooleanField(default=False)
    verified_date = models.DateTimeField(blank=True, null=True)

    def __unicode__(self):
        return self.email


class Profile(models.Model):
    name = models.CharField(max_length=30)
    user = models.ForeignKey(User)
    profile_units = models.ManyToManyField(ProfileUnits)
    display_order = models.CommaSeparatedIntegerField(max_length=255,blank=True,
                                                      null=True)

    class Meta:
        unique_together = (("name", "user"),)
    
    def __unicode__(self):
        return self.name


