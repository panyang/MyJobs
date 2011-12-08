from django.forms import ModelForm
from django.views.generic import ListView
from django.
class CreateShortyForm(ModelForm):
    """Allows users to create short URLs"""

    class Meta:
        model = shorty


class ShortyListView(ListView):
    
