from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate
from myjobs.models import *

class CustomAuthForm(AuthenticationForm):
    """
    Custom login form based on Django's default login form. This allows us to
    bypass the is_active check on the user in order to allow a limited profile
    view for users that haven't activated yet.
    
    """
    username = forms.CharField(label="Email", required=True,
                               widget=forms.TextInput(
                                   attrs={'placeholder': 'Email',
                                          'id':'id_email'}))
    password = forms.CharField(label="Password", required=True,
                               widget=forms.PasswordInput(
                                   attrs={'placeholder':'Password',
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
                raise forms.ValidationError(("Please enter a correct username and " + \
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

        
class RegistrationForm(forms.Form):
    email = forms.EmailField(label="Email", required=True,
                             widget=forms.TextInput(attrs={
                                 'placeholder': 'Email', 
                                 'id':'id_email',
                                 'autocomplete':'off'}),
                             max_length=255)
    password1 = forms.CharField(label="Password", required=True,
                                widget=forms.PasswordInput(attrs={
                                    'placeholder':'Password',
                                    'id':'id_password1',
                                    'autocomplete':'off'},
                                    render_value=False))
    password2 = forms.CharField(label="Password (again)", required=True,
                                widget=forms.PasswordInput(attrs={
                                    'placeholder': 'Password (again)',
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
            raise forms.ValidationError(("A user with that email already exists."))
        else:
            return self.cleaned_data['email']

    def clean(self):
        """
        Verify that the values entered into the two password fields
        match.
        
        """
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError(("The two password fields didn't match."))
            else:
                return self.cleaned_data
