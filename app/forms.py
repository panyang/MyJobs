from django.template import loader, Context
from django.utils.translation import ugettext_lazy as _
from django.utils.http import int_to_base36
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.models import User
from django.contrib.sites.models import get_current_site
from django.core.validators import validate_email, ValidationError
from django import forms
from app.sendgrid import SmtpApiHeader
import logging

log = logging.getLogger(__name__)

class EditUserProfile(forms.Form):
    """Form that lets user quickly edit their personal settings"""    
    first_name = forms.CharField(label=_("First Name"), 
                                 max_length=40)
    last_name = forms.CharField(label=_("Last Name"),
                                max_length=40)
    email = forms.EmailField(label=_("Email Address"))
    opt_in_myjobs = forms.BooleanField(label=_("Receive messages from my.jobs"))
    opt_in_dotjobs = forms.BooleanField(
        label=_('Receive messages from dotjobs site owners'), 
        help_text=_('Checking this allows employers who own\
        .jobs Career Microsites to communicate with you.'))
    activate_public_profile = forms.BooleanField(
        label=_("Activate Public Profile"),
        help_text=_("Check here to enable your public profile"))
    headline = forms.CharField(max_length=255, 
                               help_text=_("You in one senetence."))
    summary = forms.CharField(label=_("Summary"), max_length=4095,
            help_text=_("Short summary of you.", widget=forms.Textarea))
    
    def save(self):
        """saves user profile to UserProfile and auth.User models"""
        # Make sure we have a valid user
        try:
            u = User.objects.get(username__iexact=self.cleaned_data["username"])
        except DoesNotExist:
            HttpResponse("Forbidden", status=403, mimetype="text/plain")
        # first save all the auth.User stuff
        u.first_name = self.cleaned_data["first_name"]
        u.last_name = self.cleaned_data["last_name"]
        u.username = self.cleaned_data["username"]
        u.email = self.cleaned_data["email"]
        # Now the profile stuff
        u.profile.opt_in_myjobs = self.cleaned_data["opt_in_myjobs"]
        u.profile.opt_in_dotjobs = self.cleaned_data["opt_in_dotjobs"]        
        u.profile.activate_public_profile = self.cleaned_data["activate_public_profile"]
        u.profile.public_headline = self.cleaned_data["headline"]
        u.profile.public_summary = self.cleaned_data["summary"]
        # Now that it is set, save and done
        u.save()
        
