from django import forms
from myprofile.models import *


class BaseProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user',None)
        super (BaseProfileForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super(BaseProfileForm, self).save(commit=False)
        if self.user:
            instance.user = self.user
        return instance.save()

        
class NameForm(BaseProfileForm):
    given_name = forms.CharField(label="First Name", max_length=30,
                                 widget=forms.TextInput(attrs={
                                     'placeholder': 'First Name'}))
    family_name = forms.CharField(label="Last Name", max_length=30,
                                 widget=forms.TextInput(attrs={
                                     'placeholder': 'Last Name'}))
    primary = forms.BooleanField(label="Is this your primary name?",
                                 required=False)

    class Meta:
        model = Name
        exclude = ('user', 'date_created', 'date_updated', 'content_type',
        'display_name')


class SecondaryEmailForm(BaseProfileForm):
    class Meta:
        model = SecondaryEmail
        exclude = ('user', 'date_created', 'date_updated', 'content_type',
                   'verified_date')
        widgets = {
            'email': forms.TextInput(attrs={'placeholder': 'Email'}),
            'label': forms.TextInput(attrs={'placeholder': 'labeel'})
        }
