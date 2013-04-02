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

@login_required
def edit_profile(request):
    settings = {'user': request.user}
    module_list = ['Name', 'Education', 'EmploymentHistory', 'SecondaryEmail',
                   'Telephone', 'Address']
    units = request.user.profileunits_set
    profile_config = []
    for module in module_list:
        x= []
        module_config = {}
        verbose = re.sub("([a-z])([A-Z])","\g<1> \g<2>",module)
        module_units = units.filter(content_type__name=verbose.lower())
        module_config['verbose'] = verbose
        module_config['name'] = module
        for unit in module_units:
            x.append(getattr(unit, module.lower()))
        module_config['items'] = x
        
        profile_config.append(module_config)

    data_dict = {'profile_config': profile_config}
    return render_to_response('myprofile/edit_profile.html', data_dict,
                              RequestContext(request))

@login_required
def render_form(request):
    if request.method == "POST":
        module_type = request.POST.get('module')
        item_id = request.POST.get('id',None)
        model = globals()[module_type]
        form = globals()[module_type + 'Form']
        if item_id == 'new':
            form_instance = form(user=request.user, data=request.POST)
        else:
            obj = model.objects.get(id=item_id)
            form_instance = form(instance=obj, user=request.user, data=request.POST)
        if form_instance.is_valid():
            form_instance.save()
            return HttpResponse('saved')
        else:
            return HttpResponse('not saved')
    else:
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

@login_required
def delete_item(request):
    module_type = request.POST.get('module')
    item_id = request.POST.get('id')
    model = globals()[module_type]
    obj = model.objects.get(id=item_id, user=request.user)
    obj.delete()
    return HttpResponse('Deleted!')
