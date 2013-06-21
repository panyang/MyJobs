from django.contrib import admin
from django import forms

from mydashboard.models import (
    Company,
    DashboardModule,
    Microsite,
    Administrators
)
from myjobs.models import User


class CompanyForm(forms.ModelForm): 
    admins = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(), required=False,
        widget=admin.widgets.FilteredSelectMultiple('admins', False))

    def save(self, commit=True):
        added_admins = set()
        company = forms.ModelForm.save(self, commit)
        for admin in self.cleaned_data['admins']:
            added_admins.add(admin)

        del self.cleaned_data['admins']
        super(CompanyForm, self).save()

        if company.pk:
            old_users = set(company.admins.all())
            add = [user for user in added_admins if user not in old_users]
            remove = [user for user in old_users if user not in added_admins]
            for user in add:
                Administrators(admin=user, company=company).save()
            for user in remove:
                Administrators.objects.get(admin=user, company=company).delete()
        else:
            company.save()
            company.admins = added_admins
        return company
         
    class Meta: 
        model = Company

class CompanyAdmin(admin.ModelAdmin):
    form = CompanyForm

admin.site.register(Company, CompanyAdmin)
