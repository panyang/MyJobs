from django.forms import *
from django.utils.translation import ugettext_lazy as _
from django.utils.safestring import mark_safe

from myjobs.forms import BaseUserForm, make_choices
from mysearches.helpers import *
from mysearches.models import SavedSearch, SavedSearchDigest


class HorizontalRadioRenderer(RadioSelect.renderer):
    """
    Overrides the original RadioSelect renderer. The original displayed the radio
    buttons as an unordered list. This removes the unordered list, displaying just
    the radio button fields.
    """
    def render(self):
            return mark_safe(u'\n'.join([u'%s\n' % w for w in self]))


class SavedSearchForm(BaseUserForm):
    def __init__(self, *args, **kwargs):
        super(SavedSearchForm, self).__init__(*args, **kwargs)
        choices = make_choices(self.user)
        self.fields["email"] = ChoiceField(widget=Select(), choices=choices,
                                           initial=choices[0][0])

    feed = URLField(widget=HiddenInput())

    # day_of_week and day_of_month are not required in the database.
    # These clean functions ensure that it is required only when
    # the correct frequency is selected
    def clean_day_of_week(self):
        if self.cleaned_data.get('frequency', None) == 'W':
            if not self.cleaned_data['day_of_week']:
                raise ValidationError(_("This field is required."))
        return self.cleaned_data['day_of_week']

    def clean_day_of_month(self):
        if self.cleaned_data.get('frequency', None) == 'M':
            if not self.cleaned_data['day_of_month']:
                raise ValidationError(_("This field is required."))
        return self.cleaned_data['day_of_month']

    def clean(self):
        cleaned_data = self.cleaned_data
        url = cleaned_data.get('url')
        feed = cleaned_data.get('feed')

        if not feed:
            new_feed = validate_dotjobs_url(url)[1]
            if new_feed:
                cleaned_data['feed'] = new_feed
                del self._errors['feed']
        return cleaned_data

    def clean_url(self):
        rss_url = validate_dotjobs_url(self.cleaned_data['url'])[1]
        if not rss_url:
            raise ValidationError(_('This URL is not valid.'))

        # Check if form is editing existing instance and if duplicates exist
        if not self.instance.pk and SavedSearch.objects.filter(user=self.user,
                                                               url=self.cleaned_data['url']):
            raise ValidationError(_('URL must be unique.'))
        return self.cleaned_data['url']
        
    class Meta:
        model = SavedSearch
        widgets = {
            'notes': Textarea(attrs={'rows': 5, 'cols': 24}),
            'sort_by': RadioSelect(renderer=HorizontalRadioRenderer)
        }


class DigestForm(BaseUserForm):
    def __init__(self, *args, **kwargs):
        super(DigestForm, self).__init__(*args, **kwargs)
        choices = make_choices(self.user)
        self.fields["email"] = ChoiceField(widget=Select(attrs={
                                           'id': 'id_digest_email'}),
                                           choices=choices,
                                           initial=choices[0][0])

    is_active = BooleanField(label=_('Send digest results to:'),
                             widget=CheckboxInput(attrs={'id': 'id_digest_active'}),
                             required=False)
    
    class Meta:
        model = SavedSearchDigest
