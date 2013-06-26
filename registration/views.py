from django.contrib.auth import authenticate, login
from django.contrib.auth import views as auth_views
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.generic import TemplateView

from myjobs.models import *
from registration.models import ActivationProfile
from registration.forms import RegistrationForm

# New in Django 1.5. Class based template views for static pages
class RegistrationComplete(TemplateView):
    template_name = 'registration/registration_complete.html'


def register(request):
    """
    Registration form. Creates inactive user (which in turn sends an activation
    email) and redirect to registration complete page.
    
    """
    form = RegistrationForm()
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            new_user = User.objects.create_inactive_user(**form.cleaned_data)
            username=form.cleaned_data['email']
            password=form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            return HttpResponseRedirect('/accounts/register/complete/')
    return HttpResponse(json.dumps({'errors': form.errors.items()}))

def resend_activation(request):
    activation = ActivationProfile.objects.get_or_create(user=request.user, email=request.user.email)[0]
    activation.send_activation_email()
    return render_to_response('registration/resend_activation.html',
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
