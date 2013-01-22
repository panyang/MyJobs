from django.forms import *
from myprofile.models import *


class BaseProfileForm(ModelForm):
    """
    All ProfileUnit forms inherit from this model. It takes a user
    object as an initial input from the views and saves the form instance
    to that specified user.

    :Inputs:
    user - we will always pass a user object in because all ProfileUnits
    are linked to a user
    auto_id - this is a boolean that determines whether a label is displayed or
    not and is by default set to True. If we want the placeholder text to be
    displayed instead, pass in the value as False
    
    """
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user',None)
        super (BaseProfileForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super(BaseProfileForm, self).save(commit=False)
        if self.user:
            instance.user = self.user
        return instance.save()

        
class NameForm(BaseProfileForm):
    # For most fields, we can set the model in the Meta class to automatically
    # create the form fields. Since we want to alter the field name from the
    # default created by Django from the db field names, we have to define
    # these manually

    # We will always define the placeholder text for our formfields because
    # there are different instances where we'll use the label or we'll use
    # just the placeholder. The distinction is dealt with in the
    # form-error-highlight.html template and by passing in the auto_id value
    # as described above
    given_name = CharField(label="First Name", max_length=30,
                                 widget=forms.TextInput(attrs={
                                     'placeholder': 'First Name',
                                     'id':'id_given_name'
                                 }))
    family_name = CharField(label="Last Name", max_length=30,
                                 widget=forms.TextInput(attrs={
                                     'placeholder': 'Last Name',
                                 'id':'id_family_name'}))
    primary = BooleanField(label="Is this your primary name?",
                                 required=True)

    class Meta:
        form_name = "Personal Information"
        model = Name

class SecondaryEmailForm(BaseProfileForm):
    class Meta:
        form_name = "Secondary Email"
        model = SecondaryEmail
        # Here, we don't need to change the label but want to just change the
        # widget. We can alter just the widget by passing this dictionary
        widgets = {
            'email': TextInput(attrs={'placeholder': 'Email'}),
            'label': TextInput(attrs={'placeholder': 'Label'})
        }


class EducationForm(BaseProfileForm):
    class Meta:
        form_name = "Education"
        model = Education
        widgets = {
            'organization_name': TextInput(attrs={'placeholder': 'Institution'}),
            'degree_major': TextInput(attrs={'placeholder': 'Major'}),
            'degree_minor': TextInput(attrs={'placeholder': 'Minor'}),
            'degree_date': TextInput(attrs={'placeholder': 'Completion Date'}),
            'degree_name': TextInput(attrs={'placeholder': 'Degree Type'}),
            'start_date': TextInput(attrs={'placeholder': 'Start Date'}),
            'end_date': TextInput(attrs={'placeholder': 'End Date'}),
            'city_name': TextInput(attrs={'placeholder': 'City'}),
            'country_sub_division_code': forms.TextInput(attrs={'placeholder':
                                                        'State/Region'}), 
            'country_code': forms.TextInput(attrs={'placeholder': 'Country'}),
            'education_score': forms.TextInput(attrs={'placeholder': 'GPA'})
        }


class EmploymentForm(BaseProfileForm):
    class Meta:
        form_name = "Employment History"
        model = EmploymentHistory
        widgets = {
            'position_title': TextInput(attrs={'placeholder': 'Job Title'}),
            'organization_name': TextInput(attrs={'placeholder': 'Company'}),
            'end_date': TextInput(attrs={'placeholder': 'End Date'}),
            'start_date': TextInput(attrs={'placeholder': 'Start Date', 'id': 'start_date'}),
            'city_name': TextInput(attrs={'placeholder': 'City'}),
            'country_sub_division_code': TextInput(attrs={'placeholder':
                                                        'State/Region'}), 
            'country_code': TextInput(attrs={'placeholder': 'Country'}),
            'description': TextInput(attrs={'placeholder': 'Description'})
        }


class PhoneForm(BaseProfileForm):
    class Meta:
        form_name = "Phone Number"
        model = Telephone
        widgets = {
            'country_dialing': TextInput(attrs={'placeholder': 'Country Code', 'size': '3'}),
            'area_dialing': TextInput(attrs={'placeholder': 'Area Code','size': '4'}),
            'number': TextInput(attrs={'placeholder': 'Dial Number', 'size': '11'}),
            'extension': TextInput(attrs={'placeholder': 'Extension'})
         }


class AddressForm(BaseProfileForm):
    class Meta:
        form_name = "Address"
        model = Address
        widgets = {
            'label': TextInput(attrs={'placeholder': 'Label'}),
            'address_line_one': TextInput(attrs={'placeholder': 'Street Address 1'}),
            'address_line_two': TextInput(attrs={'placeholder': 'Street Address 2'}),
            'unit': TextInput(attrs={'placeholder': 'Apartment/Unit Number'}),
            'city_name': TextInput(attrs={'placeholder': 'City'}),
            'country_sub_division_code': TextInput(attrs={'placeholder':
                                                        'State/Region'}), 
            'country_code': TextInput(attrs={'placeholder': 'Country'}),
            'postal_code': TextInput(attrs={'placeholder': 'Zip Code'}),
            'post_office_box': TextInput(attrs={'placeholder': 'PO Box Number'})
        }
