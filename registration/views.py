from django.contrib.auth import authenticate, login
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.views.generic import TemplateView
from registration.forms import RegistrationForm
from app.models import *

class ActivationComplete(TemplateView):
    template_name = 'registration/activation_complete.html'

class RegistrationComplete(TemplateView):
    template_name = 'registration/registration_complete.html'

    
def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            new_user = User.objects.create_inactive_user(**form.cleaned_data)
            return HttpResponseRedirect('/accounts/register/complete/')
    else:
        form = RegistrationForm()
    return render_to_response('registration/registration_form.html',
                              {'form':form},
                              context_instance=RequestContext(request))

def activate(request, activation_key):
    activated = ActivationProfile.objects.activate_user(activation_key)
    ctx = {'activated': activated}
    return render_to_response('registration/activate.html',
                              ctx, context_instance=RequestContext(request))
