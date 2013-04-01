import datetime

from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import ugettext_lazy as _

from registration import signals as reg_signals
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

    def __unicode__(self):
        return self.content_type.name


class Education(ProfileUnits):
    EDUCATION_LEVEL_CHOICES = ( 
        (3, _('High School')),
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
                                                 null=True,
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
    label = models.CharField(max_length=60, verbose_name=_('Address Label'))	
    address_line_one = models.CharField(max_length=255,
                                        verbose_name=_('Street Address'))
    address_line_two = models.CharField(max_length=255, blank=True,null=True,
                                        verbose_name=_('Street Address 2'))
    unit = models.CharField(max_length=25, blank=True, null=True,
                            verbose_name=_("Apartment/Unit Number"))
    city_name = models.CharField(max_length=255, verbose_name=_("City"))
    country_sub_division_code = models.CharField(max_length=5,
                                                 verbose_name=_("State/Region"))
    country_code = models.CharField(max_length=3, verbose_name=_("Country"))
    postal_code = models.CharField(max_length=12, verbose_name=_("Zip Code"))
    post_office_box = models.CharField(max_length=60, blank=True, null=True,
                                       verbose_name=_("PO Box Number"))


class Telephone(ProfileUnits):
    USE_CODE_CHOICES = ( 
        ('Home', _('Home')),
        ('Work', _('Work')),
        ('Mobile', _('Mobile')),
        ('Pager', _('Pager')),
        ('Fax', _('Fax')),
        ('Other', _('Other')),
    )
    channel_code = models.CharField(max_length=30, editable=False)
    country_dialing = models.IntegerField(max_length=3, 
                                          verbose_name=_("Country Code"),blank=True)
    area_dialing = models.IntegerField(max_length=3, verbose_name=_("Area Code")) 
    number = models.CharField(max_length=8, verbose_name=_("Local Number"))
    extension = models.CharField(max_length=5, blank=True, null=True)
    use_code = models.CharField(max_length=30, choices=USE_CODE_CHOICES, 
    	     			        verbose_name=_("Phone Type"))
    
    def save(self, *args, **kwargs):
    	if self.use_code == "Home" or self.use_code == "Work" or self.use_code == "Other":
    	     self.channel_code = "Telephone"
    	if self.use_code == "Mobile":
    	     self.channel_code = "MobileTelephone"
    	if self.use_code == "Pager":
    	     self.channel_code = "Pager"
    	if self.use_code == "Fax":
    	     self.channel_code = "Fax"
    	super(Telephone, self).save(*args, **kwargs);


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
    display_name = models.CharField(max_length=60, blank=True, null=True,
                                    editable=False)
    primary = models.BooleanField(default=False,
                                  verbose_name=_("Is this your primary name?"))
        
    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        
        """
        full_name = '%s %s' % (self.given_name, self.family_name)
        return full_name.strip()

    def save(self, *args, **kwargs):
        if self.primary:
            try:
                temp = Name.objects.get(primary=True, pk=self.user.pk)
                if self != temp:
                    temp.primary = False
                    temp.save()
            except Name.DoesNotExist:
                pass
        super(Name, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.get_full_name()


class SecondaryEmail(ProfileUnits):
    email = models.EmailField(max_length=255)
    label = models.CharField(max_length=30, blank=True, null=True)
    verified = models.BooleanField(default=False, editable=False)
    verified_date = models.DateTimeField(blank=True, null=True, editable=False)

    def __unicode__(self):
        return self.email

    def save(self, *args, **kwargs):
        primary = kwargs.pop('old_primary', None)
        if not self.pk and primary==None:
            reg_signals.email_created.send(sender=self,user=self.user,
                                              email=self.email)
        super(SecondaryEmail,self).save(*args,**kwargs)
            
    def send_activation(self):
        reg_signals.send_activation.send(sender=self,user=self.user,
                                            email=self.email)

    def set_as_primary(self):
        """
        Replaces the User email with this email object, saves the old primary
        as a new address while maintaining the state of verification. The
        new primary address is then deleted from the SecondaryEmail table. This
        is only allowed if the email has been verified.
        Returns boolean if successful.
        """
        
        if self.verified:
            old_primary = self.user.email
            new_primary = self.email

            if self.user.is_active:
                verified=True
            else:
                verified=False

            email=SecondaryEmail(email=old_primary,verified=verified,
                                 user=self.user)
            email.save(**{'old_primary':True})
            SecondaryEmail.objects.get(email=new_primary,user=self.user).delete()
            self.user.email = new_primary
            self.user.is_active = self.verified
            self.user.save()
            return True
        else:
            return False
        
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
