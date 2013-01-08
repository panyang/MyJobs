from django import forms
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.models import get_current_site
from django.core.validators import validate_email, ValidationError
from django.template import loader, Context
from django.utils.http import int_to_base36
from django.utils.translation import ugettext_lazy as _

from myjobs.models import User

class EditProfileForm(forms.Form):
    """
    This will get deprecated anyway, no need to change it to new format
    """
    first_name = forms.CharField(label=_("First Name"), 
                                 max_length=40, required=False)
    last_name = forms.CharField(label=_("Last Name"),
                                max_length=40, required=False)
    opt_in_myjobs = forms.BooleanField(label=_("Receive messages from my.jobs"),
                                       required=False)
    def save(self,u):
        u.first_name = self.cleaned_data["first_name"]
        u.last_name = self.cleaned_data["last_name"]
        u.opt_in_myjobs = self.cleaned_data["opt_in_myjobs"]
        u.save()

        
class ChangePasswordForm(forms.Form):
    password1 = forms.CharField(label="Password",
                                widget=forms.PasswordInput(attrs={'placeholder':
                                                           'Password'}))
    password2 = forms.CharField(label="Password (again)",
                                widget=forms.PasswordInput(attrs={'placeholder':
                                                           'Password (again)'}))
    new_password = forms.CharField(label="New Password",
                                   widget=forms.PasswordInput(attrs={'placeholder':
                                                           'New Password'}))
    
    def __init__(self,*args, **kwargs):
        self.user = kwargs.pop('user',None)
        super(ChangePasswordForm, self).__init__(*args, **kwargs)

    def clean_password1(self):
        password = self.cleaned_data['password1']
        if not self.user.check_password(password):
            raise forms.ValidationError(("Wrong password."))
        else:
            return self.cleaned_data['password1']
        
    def clean(self):
        
        cleaned_data = super(ChangePasswordForm, self).clean()
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError(("The two password fields didn't match."))
            else:
                return self.cleaned_data

    def save(self):
        self.user.set_password(self.cleaned_data["new_password"])
        self.user.save()
        
        
