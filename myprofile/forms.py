from django.forms import *
from myprofile.models import *


def generate_custom_widgets(model):
    """
    Generates custom widgets and sets placeholder values and class names based
    on field type

    :Input:
    model - a model instance

    :Output:
    widgets - dictionary of widgets as defined in the Django doc
    """
    fields = model._meta.fields
    widgets = {}
    
    for field in fields:
        internal_type = field.get_internal_type()
        # exclude profile unit base fields
        if field.model == model:
            attrs = {}
            attrs['id'] = 'id_' + field.attname
            attrs['placeholder'] = field.verbose_name.title()
            if field.choices:
                widgets[field.attname] = Select()
            elif internal_type == 'BooleanField':
                widgets[field.attname] = CheckboxInput(attrs=attrs)
            else:
                widgets[field.attname] = TextInput(attrs=attrs)

    return widgets


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
    # Boolean fields must be initialized. All other field attributes generated
    # with generate_custom_widgets method
    class Meta:
        form_name = "Personal Information"
        model = Name
        widgets = generate_custom_widgets(model)
        

class SecondaryEmailForm(BaseProfileForm):
    class Meta:
        form_name = "Secondary Email"
        model = SecondaryEmail

        widgets = generate_custom_widgets(model)


class EducationForm(BaseProfileForm):
    class Meta:
        form_name = "Education"
        model = Education
        widgets = generate_custom_widgets(model)
        

class EmploymentForm(BaseProfileForm):
    class Meta:
        form_name = "Employment History"
        model = EmploymentHistory
        widgets = generate_custom_widgets(model)

        
class PhoneForm(BaseProfileForm):
    class Meta:
        form_name = "Phone Number"
        model = Telephone
        widgets = generate_custom_widgets(model)        


class AddressForm(BaseProfileForm):
    class Meta:
        form_name = "Address"
        model = Address
        widgets = generate_custom_widgets(model)
