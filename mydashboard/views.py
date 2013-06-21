import logging
import urllib2

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import user_passes_test, login_required
from django.core.urlresolvers import reverse
from django.forms.models import model_to_dict
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.utils.html import mark_safe
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView

from myjobs.models import User, EmailLog
from myjobs.forms import *
from myjobs.helpers import *
from myprofile.forms import *
from registration.forms import *

#def dashboard(request):
    #return render_to_response('mydashboard/dashboard.html')
    #render(request, 'mydashboard/dashboard.html')
    #template_name = "mydashboard/dashboard.html"
    
@user_passes_test(User.objects.not_disabled)
def mydashboard(request):
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
    
    return render_to_response('mydashboard/mydashboard.html', data_dict,
                              RequestContext(request))
    
@user_passes_test(User.objects.not_disabled)    
def profile(request):
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
    
    return render_to_response('mydashboard/profile.html', data_dict,
                              RequestContext(request))
    
@user_passes_test(User.objects.not_disabled)    
def microsites(request):
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
    
    return render_to_response('mydashboard/microsites.html', data_dict,
                              RequestContext(request))
    
@user_passes_test(User.objects.not_disabled)    
def searches(request):
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
    
    return render_to_response('mydashboard/searches.html', data_dict,
                              RequestContext(request))
    
@user_passes_test(User.objects.not_disabled)    
def jobs(request):
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
    
    return render_to_response('mydashboard/jobs.html', data_dict,
                              RequestContext(request))
