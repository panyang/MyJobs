from django import forms
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.models import get_current_site
from django.core.validators import validate_email, ValidationError
from django.template import loader, Context
from django.utils.http import int_to_base36
from django.utils.translation import ugettext_lazy as _

from myjobs.models import User
from myprofile.models import Name


class BaseUserForm(forms.ModelForm):
    """
    Most models in the other apps are associated with a user. This base form
    will take a user object as a key word argument and saves the form instance
    to a that specified user. It also takes a few common inputs that can be used
    to customize form rendering.

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
        super (BaseUserForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super(BaseUserForm, self).save(commit=False)
        if self.user:
            instance.user = self.user
        return instance.save()
    

class EditProfileForm(forms.Form):
    """
    This will get deprecated anyway, no need to change it to new format
    """
    given_name = forms.CharField(label=_("First Name"), 
                                 max_length=40)
    family_name = forms.CharField(label=_("Last Name"),
                                max_length=40)
    gravatar = forms.EmailField(label=_("Gravatar Email"))
    opt_in_myjobs = forms.BooleanField(label=_("Receive messages from my.jobs"),
                                       required=False)
    def save(self,u):
        first = self.cleaned_data['given_name']
        last = self.cleaned_data['family_name']
        try:
            obj = Name.objects.get(user=u, primary=True)
            obj.given_name = first
            obj.family_name = last
            obj.save()
        except Name.DoesNotExist:
            obj = Name(user=u, primary=True, given_name=first,family_name=last)
            obj.save()
            
        u.opt_in_myjobs = self.cleaned_data["opt_in_myjobs"]
        u.gravatar = self.cleaned_data["gravatar"]
        u.save()

        
class ChangePasswordForm(forms.Form):
    password1 = forms.CharField(label=_("Password"),
                                widget=forms.PasswordInput(attrs={'placeholder':
                                                           _('Password')}))
    password2 = forms.CharField(label=_("Password (again)"),
                                widget=forms.PasswordInput(attrs={'placeholder':
                                                           _('Password (again)')}))
    new_password = forms.CharField(label=_("New Password"),
                                   widget=forms.PasswordInput(attrs={'placeholder':
                                                           _('New Password')}))
    
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
                raise forms.ValidationError(_("The two password fields didn't match."))
            else:
                return self.cleaned_data

    def save(self):
        self.user.set_password(self.cleaned_data["new_password"])
        self.user.save()
        
        
