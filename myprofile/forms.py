from django import forms
from myprofile.models import *


class BaseProfileForm(forms.ModelForm):
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
    given_name = forms.CharField(label="First Name", max_length=30,
                                 widget=forms.TextInput(attrs={
                                     'placeholder': 'First Name',
                                     'id':'id_given_name'
                                 }))
    family_name = forms.CharField(label="Last Name", max_length=30,
                                 widget=forms.TextInput(attrs={
                                     'placeholder': 'Last Name',
                                 'id':'id_family_name'}))
    primary = forms.BooleanField(label="Is this your primary name?",
                                 required=False)

    class Meta:
        model = Name
        # Exclude any fields from ProfileUnits or Name that doesn't require user
        # input
        exclude = ('user', 'date_created', 'date_updated', 'content_type',
        'display_name')


class SecondaryEmailForm(BaseProfileForm):
    class Meta:
        model = SecondaryEmail
        exclude = ('user', 'date_created', 'date_updated', 'content_type',
                   'verified_date')
        # Here, we don't need to change the label but want to just change the
        # widget. We can alter just the widget by passing this dictionary
        widgets = {
            'email': forms.TextInput(attrs={'placeholder': 'Email'}),
            'label': forms.TextInput(attrs={'placeholder': 'Label'})
        }
