from django import forms
from savedjobs.models import *

class SaveJobForm(forms.Form):
    id = forms.IntegerField(required=False)
    title = forms.CharField(max_length=200, label="Title", widget=forms.TextInput(attrs=
                            {'placeholder': 'Title'}))
    company = forms.CharField(max_length=200, label="Company", widget=forms.TextInput(attrs=
                            {'placeholder': 'Company'}))
    city = forms.CharField(max_length=200, required=False, label="City",  widget=forms.TextInput(attrs=
                            {'placeholder': 'City'}))
    state = forms.CharField(max_length=200, required=False, label="State", widget=forms.TextInput(attrs=
                            {'placeholder': 'State'}))
    country = forms.CharField(max_length=200, required=False, label="Country",  widget=forms.TextInput(attrs=
                            {'placeholder': 'Country'}))
    url = forms.URLField(required=False, label="URL",  widget=forms.TextInput(attrs=
                            {'placeholder': 'URL'}))

    def save(self,u):
        job=SavedJob.objects.create(user=u,**self.cleaned_data)
        return job 

    def edit(self,u):
        job = SavedJob.objects.get(id=self.cleaned_data['id'])
        job.title = self.cleaned_data['title']
        job.company = self.cleaned_data['company']
        job.city = self.cleaned_data['city']
        job.state = self.cleaned_data['state']
        job.country = self.cleaned_data['country']
        job.url = self.cleaned_data['url']
        job.user = u
        job.save()
        return job

