import logging
import urllib2
import operator

from datetime import datetime, timedelta
import time
from urlparse import urlparse
from django.db.models import Q
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
from myactivity.helpers import *
from myactivity.views import *
   
@user_passes_test(lambda u: User.objects.is_group_member(u, 'Employer'))
def dashboard(request):
    """
    Returns a list of candidates who created a saved search for one of the microsites within the
    company microsite list or with the company name like jobs.jobs/company_name/careers for example
    between the given (optional) dates
    """
    
    settings = {'user': request.user}
    
    company = Company.objects.filter(admins=request.user)[0]
    admins = CompanyUser.objects.filter(company=company.id)
    microsites = Microsite.objects.filter(company=company.id)
    
    #Removes main user from admin list to display other admins
    admins = admins.exclude(user=request.user)
    
    search_microsite = request.GET.get('microsite', False)    
    
    if request.method == 'POST':
        url = request.REQUEST.get('microsite')
        #the url value for 'All' in the select box is company name 
        #which then gets replaced with all microsite urls for that company
        if url == company.name:
            microsite = [microsite.url for microsite in microsites]
        else:
            if url.find('//') == -1:
                url = '//' + url
            microsite = [urlparse(url).netloc]
        q_list = [Q(url__contains=ms) for ms in microsite]
        
        site_name = url
        
        # Saved searches were created after this date...
        if 'today' in request.POST:
            after = datetime.now()
            before = datetime.now()
        elif 'seven_days' in request.POST:
            after = datetime.now() - timedelta(days=7)
            before = datetime.now()
        elif 'thirty_days' in request.POST:
            after = datetime.now() - timedelta(days=30)
            before = datetime.now()
        else:
            after = request.REQUEST.get('after')
            if after:
                after = datetime.strptime(after, '%m/%d/%Y')
            else:
                # Defaults to one week ago
                after = datetime.now() - timedelta(days=30)
        
            before = request.REQUEST.get('before')
            if before:
                before = datetime.strptime(before, '%m/%d/%Y')
            else:
                # Defaults to the date and time that the page is accessed
                before = datetime.now()        
        
        searchescandidates = SavedSearch.objects.select_related('user')

        # All searches saved from a given microsite        
        searchescandidates = searchescandidates.filter(reduce(operator.or_, q_list))
        
        # Specific microsite searches saved between two dates
        searchescandidates = searchescandidates.filter(created_on__range=[after, before]).order_by('-created_on')           
        
    else:        
        
        #default dates and search
        after = datetime.now() - timedelta(days=30)
        before = datetime.now()
        
        if search_microsite:
            microsite=search_microsite
            searchescandidates = SavedSearch.objects.filter(url__contains=microsite)
        else:
            microsite = [microsite.url for microsite in microsites]            
            q_list = [Q(url__contains=ms) for ms in microsite]
            searchescandidates = SavedSearch.objects.select_related('user')
            searchescandidates = searchescandidates.filter(reduce(operator.or_, q_list))
            site_name = company.name
            
        searchescandidates = searchescandidates.filter(created_on__range=[after, before]).order_by('-created_on')           
            
    paginator = Paginator(searchescandidates, 5) # Show 5 candidates per page
    page = request.GET.get('page')
    
    try:
        candidates = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        candidates = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        candidates = paginator.page(paginator.num_pages)    
    
    admin_you = request.user
    
    data_dict = {'company_name': company.name,
                 'company_microsites': microsites,
                 'company_admins': admins,                 
                 'after': after,
                 'before': before,                 
                 'candidates': candidates,
                 'microsite': microsite,
                 'admin_you': admin_you,
                 'site_name': site_name,
                 'view_name': 'Company Dashboard',}
    
    return render_to_response('mydashboard/mydashboard.html', data_dict,
                              context_instance=RequestContext(request))
    


