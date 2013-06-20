from django.forms import *

from mydashboard.models import Administrators

class AdministratorsForm(ModelForm):
    """
    Administrators are only created via the admin interface and foreign key
    validation only occurs via forms even if the model contains verify_unique
    or clean methods. We must use a form to ensure correct operation
    """
    class Meta:
        model = Administrators
