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
    module_list = [('name', NameForm),
                   ('education',EducationForm),
                   ('employmenthistory', EmploymentForm),
                   ('secondaryemail', SecondaryEmailForm)]
    units = request.user.profileunits_set
    profile_config = []
    
    for module,form in module_list:
        x=[]
        module_units = units.filter(content_type__name=module)
        for unit in module_units:
            x.append(getattr(unit, module))

        profile_config.append((x, form))

    data_dict = {'profile_config': profile_config}
    return render_to_response('myprofile/edit_profile.html', data_dict,
                              RequestContext(request))
