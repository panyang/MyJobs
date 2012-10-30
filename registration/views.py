from django.contrib.auth import authenticate, login
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.views.generic import TemplateView
from registration.forms import RegistrationForm
from app.models import *

# New in Django 1.5. Class based template views for static pages
class ActivationComplete(TemplateView):
    template_name = 'registration/activation_complete.html'

class RegistrationComplete(TemplateView):
    template_name = 'registration/registration_complete.html'


def register(request):
    """
    Registration form. Creates inactive user (which in turn sends an activation
    email) and redirects to registration complete page.
    
    """
    form = RegistrationForm()
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            new_user = User.objects.create_inactive_user(**form.cleaned_data)
            return HttpResponseRedirect('/accounts/register/complete/')
    return render_to_response('registration/registration_form.html',
                              {'form':form},
                              context_instance=RequestContext(request))

def activate(request, activation_key):
    """
    Activates user and returns a boolean to activated. Activated is passed
    into the template to display an appropriate message if the activation
    passes or fails.

    Inputs:
    :activation_key: string representing an activation key for a user
    """
    activated = ActivationProfile.objects.activate_user(activation_key)
    ctx = {'activated': activated}
    return render_to_response('registration/activate.html',
                              ctx, context_instance=RequestContext(request))
