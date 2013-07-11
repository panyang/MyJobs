import logging
import urllib2
import operator

from datetime import datetime, timedelta
import time
from urlparse import urlparse
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

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
    
    # Removes main user from admin list to display other admins
    admins = admins.exclude(user=request.user)
    
    active_microsite = request.REQUEST.get('microsite', company.name)    
    
    # the url value for 'All' in the select box is company name 
    # which then gets replaced with all microsite urls for that company
    if active_microsite == company.name:
        microsite_urls = [microsite.url for microsite in microsites]
        site_name = company.name
    else:
        if active_microsite.find('//') == -1:
            active_microsite = '//' + active_microsite
        microsite_urls = [urlparse(active_microsite).netloc]
        site_name = microsite_urls[0]
    
    q_list = [Q(url__contains=ms) for ms in microsite_urls]
    
    # All searches saved on the employer's company microsites       
    candidate_searches = SavedSearch.objects.select_related('user')
    candidate_searches = candidate_searches.filter(reduce(operator.or_, q_list))
        
    # Pre-set Date ranges
    if 'today' in request.REQUEST:
        after = datetime.now()
        before = datetime.now()
    elif 'seven_days' in request.REQUEST:
        after = datetime.now() - timedelta(days=7)
        before = datetime.now()
    elif 'thirty_days' in request.REQUEST:
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
    
    # Specific microsite searches saved between two dates
    candidate_searches = candidate_searches.filter(
            created_on__range=[after, before]).order_by('-created_on')  
    
    paginator = Paginator(candidate_searches, 2) # Show 5 candidates per page
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
                 'admin_you': admin_you,
                 'site_name': site_name,
                 'view_name': 'Company Dashboard',}
    
    return render_to_response('mydashboard/mydashboard.html', data_dict,
                              context_instance=RequestContext(request))
    


