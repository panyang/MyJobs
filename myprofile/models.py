import datetime

from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import ugettext_lazy as _

from registration import signals as reg_signals
from registration.models import ActivationProfile
from myjobs.models import User


class ProfileUnits(models.Model):
    """
    This is the parent class for all user information. Creating any new
    profile unit instances (Education, Name, Email etc) end up in the
    ProfileUnits queryset as well.
    
    """
    date_created = models.DateTimeField(default=datetime.datetime.now,
                                        editable=False)
    date_updated = models.DateTimeField(default=datetime.datetime.now,
                                        editable=False)
    content_type = models.ForeignKey(ContentType, editable=False,null=True)
    user = models.ForeignKey(User, editable=False)

    def save(self, *args, **kwargs):
        """
        Custom save method to set the content type of the instance.
        
        """
        if(not self.content_type):
            self.content_type = ContentType.objects.get_for_model(self.__class__)
        super(ProfileUnits, self).save(*args, **kwargs)

    def get_fields(self):
        """
        Returns the module type, value, and field type for all
        fields on a specific model
        """
        field_list = []
        for field in self._meta.local_fields:
            if not field.primary_key:
                field_list.append([field.verbose_name.title(),
                                   self.__getattribute__(field.name),
                                   field.get_internal_type()])
        return field_list

    def __unicode__(self):
        return self.content_type.name

    def get_model_name(self):
        return self.content_type.model

    def get_verbose(self):
        return self.content_type.name.title()

    def is_displayed(self):
        return True

class Education(ProfileUnits):
    EDUCATION_LEVEL_CHOICES = (
        ('', _('Education Level')),
        (3, _('High School')),
        (4, _('Non-Degree Education')),
        (5, _('Associate')),
        (6, _('Bachelor')),
        (7, _('Master')),
        (8, _('Doctoral')),
    )
    organization_name = models.CharField(max_length=255,
                                         verbose_name=_('institution'))
    degree_date = models.DateField(verbose_name=_('completion date'))
    city_name = models.CharField(max_length=255, blank=True, null=True,
                                 verbose_name=_('city'))
    # ISO 3166-2:2007
    country_sub_division_code = models.CharField(max_length=5, blank=True,
                                                 verbose_name=_("State/Region")) 
    country_code = models.CharField(max_length=3, blank=True,
                                    verbose_name=_("country")) # ISO 3166-1
    # ISCED-2011 Can be [0-8]
    education_level_code = models.IntegerField(choices=EDUCATION_LEVEL_CHOICES,
                                               verbose_name=_("education level"))
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    education_score = models.CharField(max_length=255, blank=True,null=True,
                                       verbose_name=_("GPA"))
    degree_name = models.CharField(max_length=255, blank=True,null=True,
                                   verbose_name=_('degree type'))
    degree_major = models.CharField(max_length=255, verbose_name=_('major'))
    degree_minor = models.CharField(max_length=255, blank=True, null=True,
                                    verbose_name=_('minor'))


class Address(ProfileUnits):
    label = models.CharField(max_length=60, blank=True, 
                            verbose_name=_('Address Label'))
    address_line_one = models.CharField(max_length=255, blank=True,
                                        verbose_name=_('Address Line One'))
    address_line_two = models.CharField(max_length=255, blank=True,
                                        verbose_name=_('Address Line Two'))
    city_name = models.CharField(max_length=255, blank=True, 
                                verbose_name=_("City"))
    country_sub_division_code = models.CharField(max_length=5, blank=True,
                                                 verbose_name=_("State/Region"))
    country_code = models.CharField(max_length=3, blank=True, 
                                    verbose_name=_("Country"))
    postal_code = models.CharField(max_length=12, blank=True, 
                                    verbose_name=_("Postal Code"))


class Telephone(ProfileUnits):
    USE_CODE_CHOICES = (
        ('', 'Phone Type'),
        ('Home', 'Home'),
        ('Work', 'Work'),
        ('Mobile', 'Mobile'),
        ('Pager', 'Pager'),
        ('Fax', 'Fax'),
        ('Other', 'Other')
    )
    channel_code = models.CharField(max_length=30, editable=False, blank=True)
    country_dialing = models.CharField(max_length=3, blank=True,
                                       verbose_name=_("Country Code"))
    area_dialing = models.CharField(max_length=5, blank=True,
                                    verbose_name=_("Area Code")) 
    number = models.CharField(max_length=10, blank=True,
                              verbose_name=_("Local Number"))
    extension = models.CharField(max_length=5, blank=True)
    use_code = models.CharField(max_length=30, choices=USE_CODE_CHOICES,
                                blank=True, verbose_name=_("Phone Type"))

    def save(self, *args, **kwargs):
        if self.use_code == "Home" or self.use_code == "Work" or self.use_code == "Other":
            self.channel_code = "Telephone"
        if self.use_code == "Mobile":
            self.channel_code = "MobileTelephone"
        if self.use_code == "Pager":
            self.channel_code = "Pager"
        if self.use_code == "Fax":
            self.channel_code = "Fax"
        super(Telephone, self).save(*args, **kwargs)


class EmploymentHistory(ProfileUnits):
    position_title = models.CharField(max_length=255,verbose_name=_("Position Title"))
    organization_name = models.CharField(max_length=255,verbose_name=_("Company"))
    start_date = models.DateField(verbose_name=_("Start Date"))
    current_indicator = models.BooleanField(default=False,
                                            verbose_name=_("I still work here"))

    # Optional fields
    end_date = models.DateField(blank=True, null=True)
    city_name = models.CharField(max_length=255, blank=True,null=True)
    country_sub_division_code = models.CharField(max_length=5, blank=True,
                                                 verbose_name=_("State/Region")) 
    country_code = models.CharField(max_length=3, blank=True,null=True,
                                    verbose_name=_("country"))
    description = models.TextField(blank=True,null=True)

    # Hidden fields
    industry_code = models.CharField(max_length=255, blank=True,null=True,
                                     verbose_name=_("industry"), editable=False)
    job_category_code = models.CharField(max_length=255, blank=True,null=True,
                                         verbose_name=_("job category"), editable=False)
    onet_code = models.CharField(max_length=255, blank=True, null=True,editable=False)


class Name(ProfileUnits):
    given_name = models.CharField(max_length=30,
                                  verbose_name=_("first name"))
    family_name = models.CharField(max_length=30, 
                                   verbose_name=_("last name"))
    primary = models.BooleanField(default=False,
                                  verbose_name=_("Is primary name?"))
    
    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """

        full_name = '%s %s' % (self.given_name, self.family_name)
        return full_name.strip()

    def save(self, *args, **kwargs):
        """
        Custom name save method to ensure only one name object per user
        has primary=True. We avoid a race condition by locking the transaction
        using select_for_update.
        """
        
        if self.primary:
            try:
                temp = Name.objects.select_for_update().get(primary=True,
                                                          user=self.user)
                if self != temp:
                    temp.primary = False
                    temp.save()
            except Name.DoesNotExist:
                pass
        super(Name, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.get_full_name()

    def is_displayed(self):
        return self.primary


class SecondaryEmail(ProfileUnits):
    email = models.EmailField(max_length=255, unique=True, error_messages={
                                'unique':'This email is already registered.'})
    label = models.CharField(max_length=30, blank=True, null=True)
    verified = models.BooleanField(default=False, editable=False)
    verified_date = models.DateTimeField(blank=True, null=True, editable=False)

    def __unicode__(self):
        return self.email

    def save(self, *args, **kwargs):
        """
        Custom save triggers the creation of an activation profile and the
        sending of an activation email if the email is new.
        """

        primary = kwargs.pop('old_primary', None)
        if not self.pk and not self.verified and primary==None:
            reg_signals.email_created.send(sender=self,user=self.user,
                                           email=self.email)
            reg_signals.send_activation.send(sender=self, user=self.user,
                                             email=self.email)
        super(SecondaryEmail,self).save(*args,**kwargs)
            
    def set_as_primary(self):
        """
        Replaces the User email with this email object, saves the old primary
        as a new address while maintaining the state of verification. The
        new primary address is then deleted from the SecondaryEmail table. This
        is only allowed if the email has been verified.
        Returns boolean if successful.
        """
        
        if self.verified:
            user = self.user
            user.is_active, self.verified = self.verified, user.is_active

            self.email, user.email = user.email, self.email

            user.save()
            self.user = user
            self.save(old_primary=True)

            return True
        else:
            return False


class MilitaryService(ProfileUnits):
    MILITARY_RANK_CHOICES = (
        ('E-1', _('E-1')),
        ('E-2', _('E-2')),
        ('E-3', _('E-3')),
        ('E-4', _('E-4')),
        ('E-5', _('E-5')),
        ('E-6', _('E-6')),
        ('E-7', _('E-7')),
        ('E-8', _('E-8')),
        ('E-9', _('E-9')),
        ('O-1', _('O-1')),
        ('O-2', _('O-2')),
        ('O-3', _('O-3')),
        ('O-4', _('O-4')),
        ('O-5', _('O-5')),
        ('O-6', _('O-6')),
        ('O-7', _('O-7')),
        ('O-8', _('O-8')),
        ('O-9', _('O-9')),
        ('O-10', _('O-10')),
        ('W-1', _('W-1')),
        ('W-2', _('W-2')),
        ('W-3', _('W-3')),
        ('W-4', _('W-4')),
        ('W-5', _('W-5')),
    )
    country_code = country_code = models.CharField(max_length=3, blank=True,
                                verbose_name=_("Country")) # ISO 3166-1
    branch = models.CharField(max_length=255, 
                                help_text="Army, Navy, Air Force, etc..")
    department = models.CharField(max_length=255, blank=True, null=True,
                                verbose_name="Department")
    division = models.CharField(max_length=255, blank=True, null=True)
    expertise = models.CharField(max_length=255, blank=True, null=True, 
                help_text="Job in military")
    service_start_date = models.DateField(verbose_name=_("Start Date"))
    service_end_date = models.DateField(verbose_name=_("End Date"))
    start_rank = models.CharField(max_length=4, choices=MILITARY_RANK_CHOICES,
                                blank=True, verbose_name=_("Start Rank"))
    end_rank = models.CharField(max_length=4, choices=MILITARY_RANK_CHOICES,
                                blank=True, verbose_name=_("End Rank"))
    campaign = models.CharField(max_length=255, blank=True, null=True)
    honor = models.CharField(max_length=255, blank=True, null=True)


def delete_secondary_activation(sender, **kwargs):
    """
    When a secondary email is deleted, deletes that email's associated
    activation profile

    Inputs:
    :sender: Model that sent this signal
    :instance: instance of :sender:
    """

    instance = kwargs.get('instance')
    activation = ActivationProfile.objects.filter(user=instance.user,
                                                  email__iexact=instance.email)
    activation.delete()

# Calls `delete_secondary_activation` after a secondary email is deleted.
# dispatch_uid: arbitrary unique string that prevents this signal from
# being connected to multiple times
models.signals.pre_delete.connect(delete_secondary_activation,
                                  sender=SecondaryEmail,
                                  dispatch_uid='delete_secondary_activation')


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
