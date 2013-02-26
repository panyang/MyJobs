from django.forms import *
from mysearches.helpers import *
from mysearches.models import SavedSearch


class SavedSearchForm(ModelForm):
    feed = URLField(widget=HiddenInput())
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user',None)
        self.only_show_required = kwargs.pop('only_show_required',False)
        super (SavedSearchForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super(SavedSearchForm, self).save(commit=False)
        if self.user:
            instance.user = self.user
        return instance.save()

    def clean_day_of_week(self):
        if self.cleaned_data['frequency'] == 'W':
            if not self.cleaned_data['day_of_week']:
                raise ValidationError("This field is required.")
            self.cleaned_data['day_of_month'] = None
        return self.cleaned_data['day_of_week']

    def clean_day_of_month(self):
        if self.cleaned_data['frequency'] == 'M':
            if not self.cleaned_data['day_of_month']:
                raise ValidationError("This field is required.")
            self.cleaned_data['day_of_week'] = None
        return self.cleaned_data['day_of_month']

    def clean_url(self):
        rss_url = validate_dotjobs_url(self.cleaned_data['url'])
        if not rss_url:
            raise ValidationError('This URL is not valid.')
        return self.cleaned_data['url']

        
    class Meta:
        model = SavedSearch
