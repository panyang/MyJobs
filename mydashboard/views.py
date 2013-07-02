import logging
import urllib2

from datetime import datetime, timedelta
import time
from urlparse import urlparse

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

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
from mysearches.models import SavedSearch
from mydashboard.models import *
from myjobs.forms import *
from myjobs.helpers import *
from myprofile.forms import *
from registration.forms import *

from myactivity.views import *
   
@user_passes_test(User.objects.not_disabled)
def dashboard(request):
    """
    Notes
    """
    
    settings = {'user': request.user}
        
    company = CompanyUser.objects.get(user=request.user)
    admins = CompanyUser.objects.filter(company=company.company)
    microsites = Microsite.objects.filter(company=company.company)    
    
    #search_microsite = request.POST.get("microsite", "")    
    var1 = request.GET.get('microsite', False)
    
    #data = {}
    if request.method == 'POST':
        url = request.REQUEST.get('microsite')
        if url:
            if url.find('//') == -1:
                url = '//' + url
            microsite = urlparse(url).netloc
        else:
            microsite = 'indiana.jobs'
        #data['site'] = microsite

        # Saved searches were created after this date...
        after = request.REQUEST.get('after')
        if after:
            after = datetime.strptime(after, '%Y-%m-%d')
        else:
            # Defaults to one week ago
            after = datetime.now() - timedelta(days=7)
        # ... and before this one
        before = request.REQUEST.get('before')
        if before:
            before = datetime.strptime(before, '%Y-%m-%d')
        else:
            # Defaults to the date and time that the page is accessed
            before = datetime.now()
        #data['after'] = after
        #data['before'] = before

        # Prefetch the user
        searchescandidates = SavedSearch.objects.select_related('user')

        # All searches saved from a given microsite
        searchescandidates = searchescandidates.filter(url__contains=microsite)

        # Specific microsite searches saved between two dates
        searchescandidates = searchescandidates.filter(created_on__range=[after, before])
        #data['searches'] = searches        
        
    else:        
        
        #default dates and search
        after = datetime.now() - timedelta(days=40)
        before = datetime.now()
        #var1 = request.session.get('microsite', False)
        if var1:
            microsite=var1
        else:
            microsite='jobs.jobs'
        
        searchescandidates = SavedSearch.objects.filter(url__contains=microsite)        
        searchescandidates = searchescandidates.filter(created_on__range=[after, before])
    
    paginator = Paginator(searchescandidates, 1) # Show 5 candidates per page
    page = request.GET.get('page')
    
    try:
        candidates = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        candidates = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        candidates = paginator.page(paginator.num_pages)
    
    data_dict = {'company_name': company.company,
                 'company_microsites': microsites,
                 'company_admins': admins,                 
                 'after': after,
                 'before': before,                 
                 'candidates': candidates,
                 'microsite': microsite,}
    
    return render_to_response('mydashboard/mydashboard.html', data_dict,
                              context_instance=RequestContext(request))
    

@user_passes_test(lambda u: User.objects.is_group_member(u, 'Employer'))
def activity_search(request):
    """
    Notes
    """
    
    settings = {'user': request.user}
        
    company = CompanyUser.objects.get(user=request.user)
    admins = CompanyUser.objects.filter(company=company.company)
    microsites = Microsite.objects.filter(company=company.company)    
    
    #microsite=company.company
    
    test = request.POST.get("microsite", "")
    
    #data = {}
    if request.method == 'POST':
        url = request.REQUEST.get('microsite')
        if url:
            if url.find('//') == -1:
                url = '//' + url
            microsite = urlparse(url).netloc
        else:
            microsite = 'indiana.jobs'
        #data['site'] = microsite

        # Saved searches were created after this date...
        after = request.REQUEST.get('after')
        if after:
            after = datetime.strptime(after, '%Y-%m-%d')
        else:
            # Defaults to one week ago
            after = datetime.now() - timedelta(days=7)
        # ... and before this one
        before = request.REQUEST.get('before')
        if before:
            before = datetime.strptime(before, '%Y-%m-%d')
        else:
            # Defaults to the date and time that the page is accessed
            before = datetime.now()
        #data['after'] = after
        #data['before'] = before

        # Prefetch the user
        searchescandidates = SavedSearch.objects.select_related('user')

        # All searches saved from a given microsite
        searchescandidates = searchescandidates.filter(url__contains=microsite)

        # Specific microsite searches saved between two dates
        searchescandidates = searchescandidates.filter(created_on__range=[after, before])
        #data['searches'] = searches
    
    else:
        #default dates
        after = datetime.now() - timedelta(days=25)
        before = datetime.now()
        
        searchescandidates = SavedSearch.objects.filter(url__contains=company.company)        
        searchescandidates = searchescandidates.filter(created_on__range=[after, before])
        page = request.GET.get('page') 
        
    paginator = Paginator(searchescandidates, 3) # Show 5 candidates per page
    page = request.GET.get('page')
    
    try:
        candidates = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        candidates = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        candidates = paginator.page(paginator.num_pages)
    
    data_dict = {'company_name': company.company,
                 'company_microsites': microsites,
                 'company_admins': admins,                 
                 'after': after,
                 'before': before,                 
                 'candidates': candidates,
                 'microsite': microsite,}
    
    return render_to_response('mydashboard/candidate_activity.html', data_dict,
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
