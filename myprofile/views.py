import json
import logging
import re

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
    module_list = ['Name', 'Education', 'EmploymentHistory', 'SecondaryEmail',
                   'Telephone', 'Address']
    units = request.user.profileunits_set
    profile_config = []
    
    for module in module_list:
        x= []
        module_config = {}
        module_units = units.filter(content_type__name=module.lower())
        module_config['verbose'] = re.sub("([a-z])([A-Z])","\g<1> \g<2>",module)
        module_config['name'] = module
        
        for unit in module_units:
            x.append(getattr(unit, module.lower()))
        module_config['items'] = x
        
        profile_config.append(module_config)

    data_dict = {'profile_config': profile_config}
    return render_to_response('myprofile/edit_profile.html', data_dict,
                              RequestContext(request))


def render_form(request):
    module_type = request.GET.get('module')
    item_id = request.GET.get('id',None)
    form = globals()[module_type + 'Form']
    model = globals()[module_type]
    data_dict = {}

    if not item_id:
        form_instance = form()
        data_dict['item_id'] = 'new'
    else:
        obj = model.objects.get(id=item_id)
        form_instance = form(instance=obj)
        data_dict['item_id'] = item_id

    data_dict['module'] = module_type
    data_dict['form'] = form_instance
    return render_to_response('myprofile/profile_form.html', 
                              data_dict, RequestContext(request))
