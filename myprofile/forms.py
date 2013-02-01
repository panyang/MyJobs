from django.forms import *
from myprofile.models import *


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
                widgets[field.attname] = Select()
            elif internal_type == 'BooleanField':
                attrs['label_class'] = 'checkbox'
                widgets[field.attname] = CheckboxInput(attrs=attrs)
            else:
                widgets[field.attname] = TextInput(attrs=attrs)

    return widgets


class BaseProfileForm(ModelForm):
    """
    All ProfileUnit forms inherit from this model. It takes a user
    object as an initial input from the views and saves the form instance
    to that specified user.

    Inputs (these are the common inputs we will use for rendering forms):
    :user:       a user object. We will always pass a user object in  because all
                 ProfileUnits are linked to a user.
    :auto_id:    this is a boolean that determines whether a label is displayed or
                 not and is by default set to True. Setting this to false uses the
                 placeholder text instead, except for boolean and select fields.
    :empty_permitted: allow form to be submitted as empty even if the fields are
                 required. This is particularly useful when we combine multiple
                 Django forms on the front end and submit it as one request instead
                 of several separate requests.
    :only_show_required: Template uses this flag to determine if it should only render
                 required forms. Default is False.
    """
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user',None)
        self.only_show_required = kwargs.pop('only_show_required',False)
        super (BaseProfileForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super(BaseProfileForm, self).save(commit=False)
        if self.user:
            instance.user = self.user
        return instance.save()

class InitialNameForm(BaseProfileForm):
    primary = BooleanField(
        widget=HiddenInput(), 
        required=False, 
        initial="on")
    class Meta:
        # form_name is used in the templates to render the form header
        form_name = "Personal Information"
        model = Name
        widgets = generate_custom_widgets(model)
    
class NameForm(BaseProfileForm):
    class Meta:
        # form_name is used in the templates to render the form header
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
        form_name = "Most Recent Education"
        model = Education
        widgets = generate_custom_widgets(model)        
        

class EmploymentForm(BaseProfileForm):
    class Meta:
        form_name = "Most Recent Work History"
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
