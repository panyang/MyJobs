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
from mydashboard.models import *
from myjobs.forms import *
from myjobs.helpers import *
from myprofile.forms import *
from registration.forms import *
   
@user_passes_test(User.objects.not_disabled)
def mydashboard(request):
    """
    Notes
    """

    settings = {'user': request.user}
        
    company = Administrators.objects.get(admin=request.user)
    admins = Administrators.objects.filter(company=company.company)
    microsites = Microsite.objects.filter(company=company.company)    
    
    data_dict = {'company_name': company.company,
                 'company_microsites': microsites,
                 'company_admins': admins,}
    
    return render_to_response('mydashboard/mydashboard.html', data_dict,
                              context_instance=RequestContext(request))
    
    
@user_passes_test(User.objects.not_disabled)    
def profile(request):
    """
    Notes
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
    Notes
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
    Notes
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
    Notes
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
