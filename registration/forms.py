from django import forms
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.hashers import UNUSABLE_PASSWORD
from django.utils.translation import ugettext_lazy as _

from myjobs.models import *

class CustomAuthForm(AuthenticationForm):
    """
    Custom login form based on Django's default login form. This allows us to
    bypass the is_active check on the user in order to allow a limited profile
    view for users that haven't activated yet.
    
    """
    username = forms.CharField(label=_("Email"), required=True,
                               widget=forms.TextInput(
                                   attrs={'placeholder': _('Email'),
                                          'id':'id_email'}))
    password = forms.CharField(label=_("Password"), required=True,
                               widget=forms.PasswordInput(
                                   attrs={'placeholder':_('Password'),
                                          'id':'id_password1'},
                                   render_value=False))

    def __init__(self, request=None, *args, **kwargs):
        super(CustomAuthForm, self).__init__(request, *args, **kwargs)

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            self.user_cache = authenticate(username=username, password=password)
            if self.user_cache is None:
                raise forms.ValidationError(_("Please enter a correct username and " + \
                        "password. Note that both fields are case-sensitive."))
        self.check_for_test_cookie()
        return self.cleaned_data
        
    def check_for_test_cookie(self):
        if self.request and not self.request.session.test_cookie_worked():
            raise forms.ValidationError(self.error_messages['no_cookies'])

    def get_user_id(self):
        if self.user_cache:
            return self.user_cache.id
        return None

    def get_user(self):
        return self.user_cache


class CustomPasswordResetForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super(CustomPasswordResetForm, self).__init__(*args, **kwargs)

    def clean_email(self):
        """
        Validates that an active user exists with the given email address.
        """
        UserModel = get_user_model()
        email = self.cleaned_data["email"]
        self.users_cache = UserModel._default_manager.filter(email__iexact=email)
        if not len(self.users_cache):
            raise forms.ValidationError(self.error_messages['unknown'])
        if any((user.password == UNUSABLE_PASSWORD)
               for user in self.users_cache):
            raise forms.ValidationError(self.error_messages['unusable'])
        return email
        
        
class RegistrationForm(forms.Form):
    email = forms.EmailField(label=_("Email"), required=True,
                             widget=forms.TextInput(attrs={
                                 'placeholder': _('Email'), 
                                 'id':'id_email',
                                 'autocomplete':'off'}),
                             max_length=255)
    password1 = forms.CharField(label=_("Password"), required=True,
                                widget=forms.PasswordInput(attrs={
                                    'placeholder':_('Password'),
                                    'id':'id_password1',
                                    'autocomplete':'off'},
                                    render_value=False))
    password2 = forms.CharField(label=_("Password (again)"), required=True,
                                widget=forms.PasswordInput(attrs={
                                    'placeholder': _('Password (again)'),
                                    'id': 'id_password2',
                                    'autocomplete':'off'}, 
                                render_value=False))

    def clean_email(self):
        """
        Validate that the username is alphanumeric and is not already
        in use.
        
        """
        existing = User.objects.filter(email__iexact=self.cleaned_data['email'])
        if existing.exists():
            raise forms.ValidationError(_("A user with that email already exists."))
        else:
            return self.cleaned_data['email']

    def clean(self):
        """
        Verify that the values entered into the two password fields
        match.
        
        """
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError(_("The two password fields didn't match."))
            else:
                return self.cleaned_data
