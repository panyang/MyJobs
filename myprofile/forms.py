from django.conf import settings
from django.forms import *
from django.utils.translation import ugettext_lazy as _
from myjobs.forms import BaseUserForm
from myprofile.models import *
from countries import COUNTRIES


def generate_custom_widgets(model):
    """
    Generates custom widgets and sets placeholder values and class names based
    on field type

    Inputs:
    :model:       model class from form Meta
    
    Outputs:
    :widgets:     dictionary of widgets with custom attributes defined
    """
    fields = model._meta.fields
    widgets = {}
    
    for field in fields:
        internal_type = field.get_internal_type()
        # exclude profile unit base fields
        if field.model == model:
            attrs = {}
            attrs['id'] = 'id_' + model.__name__.lower() + '-' + field.attname
            attrs['placeholder'] = field.verbose_name.title()
            if field.choices:
                widgets[field.attname] = Select(attrs=attrs)
            elif internal_type == 'BooleanField':
                attrs['label_class'] = 'checkbox'
                widgets[field.attname] = CheckboxInput(attrs=attrs)
            elif internal_type == 'DateField':
                widgets[field.attname] = DateInput(
                                            format=settings.FORM_DATE_FORMAT,
                                            attrs=attrs)
            else:
                widgets[field.attname] = TextInput(attrs=attrs)

    return widgets


class NameForm(BaseUserForm):
    class Meta:
        # form_name is used in the templates to render the form header
        form_name = _("Personal Information")
        model = Name
        widgets = generate_custom_widgets(model)
        
        
class SecondaryEmailForm(BaseUserForm):
    class Meta:
        form_name = _("Secondary Email")
        model = SecondaryEmail
        widgets = generate_custom_widgets(model)

    def clean_email(self):
        email = self.cleaned_data['email']
        user = self.user
        if email.lower() == self.user.email.lower():
            raise forms.ValidationError('This email is already registered.')
        return email
            

class EducationForm(BaseUserForm):
    def __init__(self, *args, **kwargs):
        super(EducationForm, self).__init__(*args, **kwargs)
        self.fields['degree_date'].input_formats = settings.DATE_INPUT_FORMATS
        self.fields['start_date'].input_formats = settings.DATE_INPUT_FORMATS
        self.fields['end_date'].input_formats = settings.DATE_INPUT_FORMATS

    class Meta:
        form_name = _("Education")
        model = Education
        widgets = generate_custom_widgets(model)
        widgets['start_date'].attrs['placeholder'] = 'ie 05/30/2005'
        widgets['end_date'].attrs['placeholder'] = 'ie 06/01/2007'
        

class EmploymentHistoryForm(BaseUserForm):
    def __init__(self, *args, **kwargs):
        super(EmploymentHistoryForm, self).__init__(*args, **kwargs)
        self.fields['start_date'].input_formats = settings.DATE_INPUT_FORMATS  
        self.fields['end_date'].input_formats = settings.DATE_INPUT_FORMATS  

    class Meta:
        form_name = _("Most Recent Work History")
        model = EmploymentHistory
        widgets = generate_custom_widgets(model)
        widgets['start_date'].attrs['placeholder'] = 'ie 05/30/2005'
        widgets['end_date'].attrs['placeholder'] = 'ie 06/01/2007'
        
       
class TelephoneForm(BaseUserForm):
    """
    Returns 1 as default country code so that initial-profile-page 
    will save properly and prevent a null error.
    """
    def clean_country_dialing(self):
        country_dial = self.cleaned_data.get('country_dialing')        
        if not country_dial:
            country_dial = 1
            
        return country_dial
            
    class Meta:
        form_name = _("Phone Number")
        model = Telephone
        widgets = generate_custom_widgets(model)
        widgets['country_dialing'].attrs['class'] = "phoneCountryCode"
        widgets['area_dialing'].attrs['class'] = "phoneAreaCode"
        widgets['number'].attrs['class'] = "phoneNumber"
        widgets['extension'].attrs['class'] = "phoneExtension"
        widgets['country_dialing'].attrs['value'] = "1"
        widgets['area_dialing'].attrs['placeholder'] = "555"
        widgets['number'].attrs['placeholder'] = "555-5555"
        widgets['extension'].attrs['placeholder'] = "x1234"


class AddressForm(BaseUserForm):
    class Meta:
        form_name = _("Address")
        model = Address
        widgets = generate_custom_widgets(model)


class MilitaryServiceForm(BaseUserForm):
    def __init__(self, *args, **kwargs):
        super(MilitaryServiceForm, self).__init__(*args, **kwargs)
        self.fields['service_start_date'].input_formats = settings.DATE_INPUT_FORMATS  
        self.fields['service_end_date'].input_formats = settings.DATE_INPUT_FORMATS  

    class Meta:
        form_name = _("Military Service History")
        model = MilitaryService
        widgets = generate_custom_widgets(model)
        widgets['branch'].attrs['placeholder'] = 'Army, Navy, Air Force...'
        widgets['service_start_date'].attrs['placeholder'] = 'ie 05/30/2005'
        widgets['service_end_date'].attrs['placeholder'] = 'ie 06/01/2007'
        widgets['start_rank'].attrs['placeholder'] = 'Pay Grade ie E-4'
        widgets['end_rank'].attrs['placeholder'] = 'Pay Grade ie E-8'

    def clean_branch(self):
        return self.cleaned_data['branch'].lower()

    def clean_start_rank(self):
        return self.cleaned_data['start_rank'].upper()

    def clean_end_rank(self):
        return self.cleaned_data['end_rank'].upper()


class WebsiteForm(BaseUserForm):
    class Meta:
        form_name = _('Website')
        model = Website
        widgets = generate_custom_widgets(model)
        

class InitialForm(BaseUserForm):
    def __init__(self, *args, **kwargs):
        super(InitialForm, self).__init__(*args, **kwargs)
        for key, field in self.fields.items():
            if isinstance(field.widget, TextInput) or \
                isinstance(field.widget, Textarea) or \
                isinstance(field.widget, DateInput) or \
                isinstance(field.widget, DateTimeInput) or \
                isinstance(field.widget, TimeInput):
                field.widget.attrs.update({'placeholder': field.label})

class InitialNameForm(InitialForm):
    class Meta:
        model = Name
        fields = ['given_name', 'family_name']


class InitialAddressForm(InitialForm):
    class Meta:
        model = Address
        fields = ['address_line_one', 'address_line_two', 'city_name',
                  'country_sub_division_code', 'country_code', 'postal_code']
        widgets = { 'country_code': Select(choices=COUNTRIES) }


class InitialPhoneForm(InitialForm):
    class Meta:
        model = Telephone
        fields = ['area_dialing', 'number', 'extension', 'use_code']


class InitialWorkForm(InitialForm):
    def __init__(self, *args, **kwargs):
        super(InitialWorkForm, self).__init__(*args, **kwargs)
        self.fields['start_date'].input_formats = settings.DATE_INPUT_FORMATS

    class Meta:
        model = EmploymentHistory
        fields = ['position_title', 'organization_name', 'start_date',
                 'current_indicator']


class InitialEducationForm(InitialForm):
    def __init__(self, *args, **kwargs):
        super(InitialEducationForm, self).__init__(*args, **kwargs)
        self.fields['degree_date'].input_formats = settings.DATE_INPUT_FORMATS

    class Meta:
        model = Education
        fields = ['organization_name', 'degree_date', 'education_level_code',
                  'degree_name']
