import json
import logging

from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.forms.models import model_to_dict
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.views.generic import TemplateView

from myjobs.forms import *
from myjobs.helpers import *
from myprofile.forms import *
from registration.forms import *

def edit_profile(request):
    settings = {'user': request.user}
    if request.method == "POST":
        forms = instantiate_profile_forms(request, [NameForm, EducationForm], settings,
                                  post=True)
        for form in forms:
            if form.is_valid():
                form.save()
    else:
        forms = instantiate_profile_forms(request, [NameForm, EducationForm], settings)

    data_dict = {'forms': forms}
    return render_to_response('myprofile/edit_profile.html', data_dict,
                              RequestContext(request))
