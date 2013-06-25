from django.forms import *
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.models import get_current_site
from django.core.validators import validate_email, ValidationError
from django.template import loader, Context
from django.utils.http import int_to_base36
from django.utils.translation import ugettext_lazy as _

from myjobs.models import User
from myprofile.models import Name, SecondaryEmail

def make_choices(user):
    choices = [(user.email, user.email)]
    for email in SecondaryEmail.objects.filter(user=user, verified=True):
        choices.append((email.email, email.email))
    return choices

class BaseUserForm(ModelForm):
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
    

class EditAccountForm(Form):
    given_name = CharField(label=_("First Name"),
                            widget=TextInput(attrs={'placeholder': 'First Name'}),
                                 max_length=40, required=False)
    family_name = CharField(label=_("Last Name"),
                            widget=TextInput(attrs={'placeholder': 'Last Name'}),
                                max_length=40, required=False)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user',None)
        self.choices = make_choices(self.user)
        super(EditAccountForm, self).__init__(*args, **kwargs)
        self.fields["gravatar"] = ChoiceField(label=_("Gravatar Email"),
                                              widget=Select(attrs=
                                            {'id':'id_gravatar'}),
                                              choices=self.choices,
                                              initial=self.choices[0][0])

    def clean(self):
        cleaned_data = super(EditAccountForm, self).clean()
        first = cleaned_data.get("given_name")
        last = cleaned_data.get("family_name")

        # Exclusive or. These fields must either both exist or not at all
        if bool(first) != bool(last):
            error_msg = u"Both a first and last name required."
            self._errors["given_name"] = self.error_class([error_msg])
            self._errors["family_name"] = self.error_class([error_msg])

            # These fields are no longer valid. Remove them from the
            # cleaned data.
            del cleaned_data["given_name"]
            del cleaned_data["family_name"]
        
        return cleaned_data
    

    def save(self, u):
        first = self.cleaned_data.get("given_name", None)
        last = self.cleaned_data.get("family_name", None)

        try:
            obj = Name.objects.get(user=u, primary=True)
            if not first and not last:
                obj.delete()
            else:
                obj.given_name = first
                obj.family_name = last
                obj.save()
        except Name.DoesNotExist:
            obj = Name(user=u, primary=True, given_name=first,
                       family_name=last)
            obj.save()

        u.gravatar = self.cleaned_data["gravatar"]
        u.save()


class EditCommunicationForm(BaseUserForm):
    def __init__(self, *args, **kwargs):
        super(EditCommunicationForm,self).__init__(*args, **kwargs)
        choices = make_choices(self.user)
        self.fields["email"] = ChoiceField(widget=Select(attrs={
                                           'id':'id_digest_email'}),
                                           choices=choices,
                                           initial=choices[0][0])
        self.fields["email"].label = "Primary Email:"

    def save(self):
        if self.cleaned_data['email'] != self.user.email:
            new_email = SecondaryEmail.objects.get(
                email__iexact=self.cleaned_data['email'])
            if new_email.verified:
                new_email.set_as_primary()
            else:
                self.cleaned_data['email'] = self.user.email
        super(EditCommunicationForm, self).save(self)

    class Meta:
        model = User
        fields = ('email', 'opt_in_employers')


class ChangePasswordForm(Form):
    password = CharField(label="Password",
                                widget=PasswordInput(attrs={'placeholder':'Password'}))
    new_password1 = CharField(label="New Password",
                                widget=PasswordInput(attrs={'placeholder':'New Password'}))
    new_password2 = CharField(label="New Password (again)",
                                widget=PasswordInput(attrs={'placeholder':'New Password (again)'}))
    
    def __init__(self,*args, **kwargs):
        self.user = kwargs.pop('user',None)
        super(ChangePasswordForm, self).__init__(*args, **kwargs)

    def clean_password(self):
        password = self.cleaned_data['password']
        if not self.user.check_password(password):
            raise ValidationError(("Wrong password."))
        else:
            return self.cleaned_data['password']
        
    def clean(self):
        cleaned_data = super(ChangePasswordForm, self).clean()
        if 'new_password1' in self.cleaned_data and 'new_password2' in self.cleaned_data:
            if self.cleaned_data['new_password1'] != self.cleaned_data['new_password2']:
                error_msg = u"The new password fields did not match."
                self._errors["new_password1"] = self.error_class([error_msg])
                self._errors["new_password2"] = self.error_class([error_msg])

                # These fields are no longer valid. Remove them from the
                # cleaned data.
                del cleaned_data["new_password1"]
                del cleaned_data["new_password2"]
                #raise forms.ValidationError(_("The two new password fields did not match."))
            else:
                return self.cleaned_data

    def save(self):
        self.user.set_password(self.cleaned_data["new_password1"])
        self.user.save()    
