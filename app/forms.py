from django.template import loader, Context
from django.utils.translation import ugettext_lazy as _
from django.utils.http import int_to_base36
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.models import get_current_site
from django.core.validators import validate_email, ValidationError
from django import forms
from app.models import User

class EditProfileForm(forms.Form):
    """Form that lets user quickly edit their personal settings"""    
    first_name = forms.CharField(label=_("First Name"), 
                                 max_length=40, required=False)
    last_name = forms.CharField(label=_("Last Name"),
                                max_length=40, required=False)
    opt_in_myjobs = forms.BooleanField(label=_("Receive messages from my.jobs"),
                                       required=False)
    opt_in_dotjobs = forms.BooleanField(label=_('Receive messages from dotjobs site owners'), 
                                        required=False)
    activate_public_profile = forms.BooleanField(label=_("Activate Public Profile"),
                                                 required=False)
    headline = forms.CharField(max_length=255, required=False)
    summary = forms.CharField(widget=forms.widgets.Textarea(), label=_("Summary"),
                              required=False, max_length=4095)
    
    def save(self,u):
        """saves user profile to UserProfile and auth.User models"""
        # first save all the auth.User stuff
        u.first_name = self.cleaned_data["first_name"]
        u.last_name = self.cleaned_data["last_name"]
        # Now the profile stuff
        u.opt_in_myjobs = self.cleaned_data["opt_in_myjobs"]
        u.opt_in_dotjobs = self.cleaned_data["opt_in_dotjobs"]        
        u.activate_public_profile = self.cleaned_data["activate_public_profile"]
        u.public_headline = self.cleaned_data["headline"]
        u.public_summary = self.cleaned_data["summary"]
        # Now that it is set, save and done
        u.save()
        
