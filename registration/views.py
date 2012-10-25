from django.contrib.auth import authenticate, login
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from registration.forms import RegistrationForm
from app.models import *

def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            new_user = User.objects.create_inactive_user(**form.cleaned_data)
            return HttpResponseRedirect('/registration/registration_complete.html')
    return render_to_response('registration/registration_form.html',
                              context_instance=RequestContext(request))

