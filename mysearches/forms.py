from django.forms import *
from django.utils.translation import ugettext_lazy as _

from myjobs.forms import BaseUserForm, make_choices
from mysearches.helpers import *
from mysearches.models import SavedSearch, SavedSearchDigest
from myprofile.models import SecondaryEmail


class SavedSearchForm(BaseUserForm):
    def __init__(self, *args, **kwargs):
        super(SavedSearchForm, self).__init__(*args, **kwargs)
        choices = make_choices(self.user)
        self.fields["email"] = ChoiceField(widget=Select(), choices=choices,
                                           initial=choices[0][0])
        

    feed = URLField(widget=HiddenInput())

    # day_of_week and day_of_month are not required in the database.
    # These clean functions ensure that it is required only when
    # the correct frequency is selected and clears any remaining
    # day_of_week/day_of_month data that shouldn't be there
    def clean_day_of_week(self):
        if self.cleaned_data.get('frequency', None) == 'W':
            if not self.cleaned_data['day_of_week']:
                raise ValidationError(_("This field is required."))
            self.cleaned_data['day_of_month'] = None
        return self.cleaned_data['day_of_week']

    def clean_day_of_month(self):
        if self.cleaned_data.get('frequency', None) == 'M':
            if not self.cleaned_data['day_of_month']:
                raise ValidationError(_("This field is required."))
            self.cleaned_data['day_of_week'] = None
        return self.cleaned_data['day_of_month']

    def clean_url(self):
        rss_url = validate_dotjobs_url(self.cleaned_data['url'])[0]
        if not rss_url:
            raise ValidationError(_('This URL is not valid.'))
        return self.cleaned_data['url']
        
    class Meta:
        model = SavedSearch


class DigestForm(BaseUserForm):
    def __init__(self, *args, **kwargs):
        super(DigestForm, self).__init__(*args, **kwargs)
        choices = make_choices(self.user)
        self.fields["email"] = ChoiceField(widget=Select(attrs={
                                           'id':'id_digest_email'}),
                                           choices=choices,
                                           initial=choices[0][0])

    is_active = BooleanField(label=_('Send my results in a single digest email'
                             ' to:'), widget=CheckboxInput(
                             attrs={'id':'id_digest_active'}))
    
    class Meta:
        model = SavedSearchDigest
