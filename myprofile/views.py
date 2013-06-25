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
    """
    Main profile view that the user first sees. Ultimately generates the
    following in data_dict:

    :profile_config: A list of dictionaries. Each dictionary represents a
                     different module (based on module_list) with the keys:
                     verbose - the displayable title of the module
                     name - the module name as it's named in the models.
                     items - all the instances in that module for the user

    :name_obj:       The name of the user or, if not provided, the user's email
    """

    settings = {'user': request.user}
    module_list = ['Name', 'Education', 'EmploymentHistory', 'SecondaryEmail',
                   'Telephone', 'Address']
    units = request.user.profileunits_set
    profile_config = []
    
    for module in module_list:
        model = globals()[module]
        verbose = model._meta.verbose_name

        x= []
        module_config = {}
        module_units = units.filter(content_type__name=verbose)

        module_config['verbose'] = verbose.title()
        module_config['name'] = module
        for unit in module_units:
            if hasattr(unit, module.lower()):
                x.append(getattr(unit, module.lower()))
        module_config['items'] = x
        
        profile_config.append(module_config)

    data_dict = {'profile_config': profile_config,        
                 'name_obj': get_name_obj(request)}
    
    return render_to_response('myprofile/edit_profile.html', data_dict,
                              RequestContext(request))

@user_passes_test(User.objects.not_disabled)
def handle_form(request):
    """
    All profile forms are routed through here. On a GET, it returns
    the form. On a valid POST, it renders the profile item to be appended
    to the existing profile. On an invalid post, it returns a JSON dump of
    all the errors. The data_dict includes the following:

    :module:          camel case name of the module
    :first_instance:  boolean
    :item_id:         ID of the form item if it exists. If it doesn't, it is the
                      string 'new'
    :form:            Form instance
    
    """
    module_type = request.REQUEST.get('module')
    first_instance = request.REQUEST.get('first_instance')
    if first_instance:
        first_instance = int(first_instance)

    item_id = request.REQUEST.get('id', None)
    model = globals()[module_type]
    # This assumes that form names follow the convention 'moduleForm'
    form = globals()[module_type + 'Form']
    data_dict = {'module': module_type,'first_instance':first_instance}
    verbose = model._meta.verbose_name.title()

    if request.method == "POST":
        data_dict['name'] = module_type

        #Handles requests to resend activation email
        if request.POST.get("action") == "updateEmail":
            obj = model.objects.get(id=item_id)
            activation = ActivationProfile.objects.get(email=obj.email)
            activation.send_activation_email(primary=False)
            return render_to_response('myprofile/profile_item.html', data_dict,
                                      RequestContext(request))
        else:
            if item_id == 'new':
                form_instance = form(user=request.user, data=request.POST,
                                     auto_id=False)
                if first_instance:
                    template = 'myprofile/profile_section.html'
                    data_dict['verbose'] = verbose
                else:
                    template = 'myprofile/profile_item.html'
            else:
                obj = model.objects.get(id=item_id)
                form_instance = form(instance=obj, user=request.user, data=request.POST,
                                     auto_id=False)
                template = 'myprofile/profile_item.html'

            if form_instance.is_valid():
                form_instance.save()
                if first_instance:
                    data_dict['items'] = [form_instance.instance]
                    data_dict = {'module': data_dict}
                else:
                    data_dict['item'] = form_instance.instance
                return render_to_response(template, data_dict,
                                          RequestContext(request))
            else:
                return HttpResponse(json.dumps({'errors': form_instance.errors.items()}))
    else:
        if not item_id or item_id == 'new':
            form_instance = form(auto_id=False)
            data_dict['item_id'] = 'new'
        else:
            obj = model.objects.get(id=item_id)
            form_instance = form(instance=obj, auto_id=False)
            data_dict['item_id'] = item_id
            
            #Used to determine whether or not to display resend activation email link
            if data_dict['module'] == "SecondaryEmail":
                data_dict['verified'] = obj.verified

        data_dict['verbose'] = verbose
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
def get_details(request):
    module = request.GET.get('module')
    module_config = {}
    item_id = request.GET.get('id')
    model = globals()[module]
    module_config['verbose'] = model._meta.verbose_name.title()
    module_config['name'] = module
    try:
        obj = model.objects.get(id=item_id, user=request.user)
    except model.DoesNotExist:
        return HttpResponse('Item not found')
    module_config['item'] = obj
    data_dict = {'module': module_config}
    return render_to_response('myprofile/profile_details.html',
                              data_dict, RequestContext(request))
