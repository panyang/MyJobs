import json
import logging
import re

from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.urlresolvers import reverse
from django.forms.models import model_to_dict
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.views.generic import TemplateView

from myjobs.models import User
from myjobs.forms import *
from myjobs.helpers import *
from myprofile.forms import *
from registration.forms import *

@user_passes_test(User.objects.not_disabled)
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

    data_dict = {
        'profile_config': profile_config,        
        'name_obj': get_name_obj(request)}
    return render_to_response('myprofile/edit_profile.html', data_dict,
                              RequestContext(request))

@user_passes_test(User.objects.not_disabled)
def handle_form(request):
    module_type = request.REQUEST.get('module')
    first_instance = request.REQUEST.get('first_instance')
    if first_instance:
        first_instance = int(first_instance)

    item_id = request.REQUEST.get('id', None)
    model = globals()[module_type]
    form = globals()[module_type + 'Form']
    data_dict = {'module': module_type,'first_instance':first_instance}

    if request.method == "POST":
        if item_id == 'new':            
            form_instance = form(user=request.user, data=request.POST)
        else:
            obj = model.objects.get(id=item_id)
            form_instance = form(instance=obj, user=request.user, data=request.POST)

        if form_instance.is_valid():
            item = form_instance.save()
            data_dict['item'] = form_instance.instance
            return render_to_response('myprofile/profile_item.html', data_dict,
                                      RequestContext(request))
        else:
            data_dict['item_id'] = item_id
            data_dict['form'] = form_instance
            return render_to_response('myprofile/profile_form.html', data_dict,
                                      RequestContext(request))
    else:
        if not item_id:
            form_instance = form()
            data_dict['item_id'] = 'new'
        else:
            obj = model.objects.get(id=item_id)
            form_instance = form(instance=obj)
            data_dict['item_id'] = item_id

        data_dict['form'] = form_instance
        return render_to_response('myprofile/profile_form.html', 
                                  data_dict, RequestContext(request))


@user_passes_test(User.objects.not_disabled)
def delete_item(request):
    module_type = request.POST.get('module')
    item_id = request.POST.get('id')
    model = globals()[module_type]
    obj = model.objects.get(id=item_id, user=request.user)
    obj.delete()
    return HttpResponse('Deleted!')


@user_passes_test(User.objects.not_disabled)
def add_section(request):
    module = request.GET.get('module')
    module_config = {}
    verbose = re.sub("([a-z])([A-Z])","\g<1> \g<2>",module)
    module_config['verbose'] = verbose
    module_config['name'] = module
    module_config['items'] = None

    data_dict = {'module': module_config}
    return render_to_response('myprofile/profile_section.html',
                              data_dict, RequestContext(request))
