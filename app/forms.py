from django.template import loader, Context
from django.utils.translation import ugettext_lazy as _
from django.utils.http import int_to_base36
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.models import User
from django.contrib.sites.models import get_current_site
from django.core.validators import validate_email, ValidationError
from django import forms
from app.models import UserProfile
from app.sendgrid import SmtpApiHeader
import logging

log = logging.getLogger(__name__)

def validate_unique_user(value):
    if value == User.objects.get(username__iexact=value):
        raise ValidationError(_("%s is not available." % value))
    
class GetMissingRegistrationData(forms.Form):
    """Form for getting missing email and username from users who social auth"""
    username = forms.charField(label=_("Username"), max_length=80,
                               validators=[validate_unique_user])
    email = forms.EmailField(label=_("Email Address"),
        help_text=_("Having an email address allows you\
        to retrieve your account settings"))

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
    headline = forms.CharField(max_length=255, null=True, blank=True, 
                               help_text=_("You in one senetence."))
    summary = forms.Textarea(label=_("Summary"), null=True, blank=True,
        help_text=_("A brief summary of your experience."))
    
    def save(self, username):
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

  
    class CredentialResetForm(forms.Form):
        credential = forms.CharField(label=_("Username or Email"),
                            max_length=75)

    users_cache = []

    def clean_credential(self):
        """
        Validates that a user exists
        """
        credential = self.cleaned_data["credential"]
        try:
            validate_email(credential)
        except ValidationError:
            # we don't have an email address.
            # so we need to see if we have a username
            self.users_cache = User.objects.filter(
                                username__iexact=credential,
                                is_active=True)
            if len(self.users_cache) == 0:
                raise ValidationError(_("No user with this name exists."))
        else:
            # we have an email address
            self.users_cache = User.objects.filter(
                                 email__iexact=credential,
                                 is_active=True)
        # make sure at least one user is associated with this email address.
        if len(self.users_cache) == 0:
            raise forms.ValidationError(_("No my.jobs accounts exist for this email."))
        return credential

    def save(self, domain_override=None,
             email_template_name='registration/multi_reset_email.html',
             use_https=False, token_generator=default_token_generator,
             from_email=None, request=None):
        """
        Generates a list of associated accounts and one-use only links for resetting.
        """
        site_name = "my.jobs"
        from myjobs.sendgrid import send_mail_with_headers as send_mail
        c = {}
        for user in self.users_cache:
            if not domain_override:
                current_site = get_current_site(request)
                site_name = current_site.name
                domain = current_site.domain
            else:
                #site_name = domain = domain_override
                site_name = current_site.name
            c[user.username] = {'email': user.email,
                                'domain': domain,
                                'site_name': site_name,
                                'uid': int_to_base36(user.id),
                                'user': user,
                                'token': token_generator.make_token(user),
                                'protocol': use_https and 'https' or 'http',
                                }
        # set the context
        credentials = {'credentials': c}
        credentials['site_name'] = site_name
        # set SendGrid Headers
        h = SmtpApiHeader()
        h.setCategory("transactional")
        # prevent password recovery keys from showing up in sendgrid history
        # h.addFilterSetting('clicktrack','enable', 0)
        t = loader.get_template(email_template_name)
        send_mail(_("Password reset on %s") % site_name,
                  t.render(Context(credentials)),
                  from_email, [user.email], headers=h.as_django_email_header())
