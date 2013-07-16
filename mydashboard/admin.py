from django.contrib import admin
from django import forms

from mydashboard.models import (
    Company,
    DashboardModule,
    Microsite,
    CompanyUser
)
from myjobs.models import User


class CompanyForm(forms.ModelForm): 
    """
    Django needs help to do m2m relations in the admin interface.

    What this does is add a multiple choice box to allow the addition and
    deletion of multiple CompanyUser instances at once. When the form is saved,
    those instances are manually created/deleted and then they are removed from
    the cleaned_data dict to make the form valid again.
    """
    admins = forms.ModelMultipleChoiceField(
        queryset=User.objects.filter(groups__name=CompanyUser.GROUP_NAME), required=False,
        widget=admin.widgets.FilteredSelectMultiple('admins', False))

    def save(self, commit=True):
        added_users = set()
        company = forms.ModelForm.save(self, commit)
        for user in self.cleaned_data['admins']:
            added_users.add(user)

        del self.cleaned_data['admins']
        super(CompanyForm, self).save()

        if company.pk:
            old_users = company.admins.all()
            add = [user for user in added_users if user not in old_users]
            remove = [user for user in old_users if user not in added_users]
            for user in add:
                CompanyUser(user=user, company=company).save()
            for user in remove:
                CompanyUser.objects.get(user=user, company=company).delete()
        else:
            company.save()
            company.admins = added_users
        return company
         
    class Meta: 
        model = Company

class CompanyAdmin(admin.ModelAdmin):
    form = CompanyForm

admin.site.register(Company, CompanyAdmin)

admin.site.register(Microsite)
