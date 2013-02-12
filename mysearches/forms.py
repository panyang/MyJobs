from django.forms import *
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

    class Meta:
        model = SavedSearch
