from django.forms import *

from mydashboard.models import CompanyUser

class CompanyUserForm(ModelForm):
    """
    CompanyUsers are only created via the admin interface and foreign key
    validation only occurs via forms even if the model contains verify_unique
    or clean methods. We must use a form to ensure correct operation
    """
    class Meta:
        model = CompanyUser
