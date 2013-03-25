from django.forms import *
from django.utils.translation import ugettext_lazy as _

from myjobs.forms import BaseUserForm
from mysearches.helpers import *
from mysearches.models import SavedSearch, SavedSearchDigest


class SavedSearchForm(BaseUserForm):
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
    is_active = BooleanField(label=_('Send my results in a single digest email to:'), widget=CheckboxInput(
                                 attrs={'id':'id_digest_active'}))
    email = CharField(label=_('Send results to'), widget=TextInput(attrs=
                                       {'id':'id_digest_email'}))
    
    class Meta:
        model = SavedSearchDigest
