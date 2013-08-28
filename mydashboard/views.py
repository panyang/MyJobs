import operator

from datetime import datetime, timedelta

from django.contrib.auth.decorators import user_passes_test
from django.db.models import Q
from django.http import Http404
from django.template import RequestContext
from django.shortcuts import render_to_response

from mydashboard.helpers import saved_searches
from mydashboard.models import *
from myjobs.models import User, PrimaryNameProfileUnitManager
from mysearches.models import SavedSearch
from endless_pagination.decorators import page_template


@page_template("mydashboard/dashboard_activity.html")
@user_passes_test(lambda u: User.objects.is_group_member(u, 'Employer'))
def dashboard(request, template="mydashboard/mydashboard.html",
              extra_context=None, company=None):
    """
    Returns a list of candidates who created a saved search for one of the
    microsites within the company microsite list or with the company name like
    jobs.jobs/company_name/careers for example between the given (optional)
    dates

    Inputs:
    :company:               company.id that is associated with request.user

    Returns:
    :render_to_response:    renders template with context dict
    """

    company_id = request.REQUEST.get('company')
    if company_id is None:
        try:
            company = Company.objects.filter(admins=request.user)[0]
        except Company.DoesNotExist:
            raise Http404

    context = {
        'candidates': SavedSearch.objects.all(),
    }

    if not company:
        try:
            company = Company.objects.get(admins=request.user, id=company_id)
        except:
            raise Http404

    admins = CompanyUser.objects.filter(company=company.id)
    authorized_microsites = Microsite.objects.filter(company=company.id)
    
    # Removes main user from admin list to display other admins
    admins = admins.exclude(user=request.user)
    requested_microsite = request.REQUEST.get('microsite', company.name)
    requested_after_date = request.REQUEST.get('after', False)
    requested_before_date = request.REQUEST.get('before', False)
    requested_date_button = request.REQUEST.get('date_button', False)    
                
    # the url value for 'All' in the select box is company name 
    # which then gets replaced with all microsite urls for that company
    site_name = ''
    if requested_microsite != company.name:
        if requested_microsite.find('//') == -1:
            requested_microsite = '//' + requested_microsite
        active_microsites = authorized_microsites.filter(
            url__contains=requested_microsite)
        
    else:
        active_microsites = authorized_microsites
        site_name = company.name
        
    microsite_urls = [microsite.url for microsite in active_microsites]
    if not site_name:
        site_name = microsite_urls[0]

    q_list = [Q(url__contains=ms) for ms in microsite_urls]
    
    # All searches saved on the employer's company microsites       
    candidate_searches = SavedSearch.objects.select_related('user')
    try:
        candidate_searches = candidate_searches.filter(reduce(operator.or_, q_list))
    except:
        raise Http404
        
    # Pre-set Date ranges
    if 'today' in request.REQUEST:
        after = datetime.now() - timedelta(days=1)
        before = datetime.now()
        requested_date_button = 'today'
    elif 'seven_days' in request.REQUEST:
        after = datetime.now() - timedelta(days=7)
        before = datetime.now()
        requested_date_button = 'seven_days'
    elif 'thirty_days' in request.REQUEST:
        after = datetime.now() - timedelta(days=30)
        before = datetime.now()
        requested_date_button = 'thirty_days'
    else:
        if requested_after_date:            
            after = datetime.strptime(requested_after_date, '%m/%d/%Y')            
        else:
            after = request.REQUEST.get('after')
            if after:
                after = datetime.strptime(after, '%m/%d/%Y')
            else:
                # Defaults to 30 days ago
                after = datetime.now() - timedelta(days=30)                
                
        if requested_before_date:
            before = datetime.strptime(requested_before_date, '%m/%d/%Y')            
        else:        
            before = request.REQUEST.get('before')
            if before:
                before = datetime.strptime(before, '%m/%d/%Y')
            else:
                # Defaults to the date and time that the page is accessed
                before = datetime.now()
    
    # Specific microsite searches saved between two dates
    candidate_searches = candidate_searches.filter(
        created_on__range=[after, before]).order_by('-created_on')
    
    admin_you = request.user
    
    context = {'company_name': company.name,
               'company_microsites': authorized_microsites,
               'company_admins': admins,
               'company_id': company.id,
               'after': after,
               'before': before,                 
               'candidates': candidate_searches,                
               'admin_you': admin_you,
               'site_name': site_name,
               'view_name': 'Company Dashboard',
               'date_button': requested_date_button,
               }
    
    if extra_context is not None:
        context.update(extra_context)
    return render_to_response(template, context,
                              context_instance=RequestContext(request))
    

@page_template("mydashboard/site_activity.html")
@user_passes_test(lambda u: User.objects.is_group_member(u, 'Employer'))
def microsite_activity(request, template="mydashboard/microsite_activity.html",
                       extra_context=None, company=None):
    """
    Returns the activity information for the microsite that was select on the
    employer dashboard page.  Candidate activity for saved searches, job
    views, etc.

    Inputs:
    :company:               company.id that is associated with request.user

    Returns:
    :render_to_response:    renders template with context dict
    """
    context = {'candidates': SavedSearch.objects.all(),
               }

    company_id = request.REQUEST.get('company')
    if company_id is None:
        try:
            company = Company.objects.filter(admins=request.user)[0]
        except Company.DoesNotExist:
            raise Http404

    if not company:
        try:
            company = Company.objects.get(admins=request.user, id=company_id)
        except:
            raise Http404
    
    requested_microsite = request.REQUEST.get('url', False)
    requested_date_button = request.REQUEST.get('date_button', False)
    requested_after_date = request.REQUEST.get('after', False)
    requested_before_date = request.REQUEST.get('before', False)
    
    if not requested_microsite:
        requested_microsite = request.REQUEST.get('microsite-hide', company.name)
    
    if requested_microsite.find('//') == -1:
            requested_microsite = '//' + requested_microsite
            
    # Pre-set Date ranges
    if 'today' in request.REQUEST:
        after = datetime.now() - timedelta(days=1)
        before = datetime.now()
        requested_date_button = 'today'
    elif 'seven_days' in request.REQUEST:
        after = datetime.now() - timedelta(days=7)
        before = datetime.now()
        requested_date_button = 'seven_days'
    elif 'thirty_days' in request.REQUEST:
        after = datetime.now() - timedelta(days=30)
        before = datetime.now()
        requested_date_button = 'thirty_days'
    else:
        if requested_after_date:            
            after = datetime.strptime(requested_after_date, '%m/%d/%Y')            
        else:
            after = request.REQUEST.get('after')
            if after:
                after = datetime.strptime(after, '%m/%d/%Y')
            else:
                # Defaults to 30 days ago
                after = datetime.now() - timedelta(days=30)                
                
        if requested_before_date:
            before = datetime.strptime(requested_before_date, '%m/%d/%Y')            
        else:        
            before = request.REQUEST.get('before')
            if before:
                before = datetime.strptime(before, '%m/%d/%Y')
            else:
                # Defaults to the date and time that the page is accessed
                before = datetime.now()
    
    # All searches saved on the employer's company microsites       
    candidate_searches = SavedSearch.objects.filter(url__contains=requested_microsite)
        
    # Specific microsite searches saved between two dates
    candidate_searches = candidate_searches.filter(
        created_on__range=[after, before]).order_by('-created_on')
    
    saved_search_count = candidate_searches.count()      
    
    context = {'microsite_url': requested_microsite,
               'after': after,
               'before': before,
               'candidates': candidate_searches,
               'view_name': 'Company Dashboard',
               'company_name': company.name,
               'company_id': company.id,
               'date_button': requested_date_button,
               'saved_search_count': saved_search_count}
    
    if extra_context is not None:
        context.update(extra_context)
    return render_to_response(template, context,
                              context_instance=RequestContext(request))


@user_passes_test(lambda u: User.objects.is_group_member(u, 'Employer'))
def candidate_information(request):
    """
    Sends user info, primary name, and searches to candidate_information.html.
    Gathers the employer's (request.user) companies and microsites and puts
    the microsites' domains in a list for further checking and logic,
    see helpers.py.
    """

    user_id = request.REQUEST.get('user')
    company_id = request.REQUEST.get('company')

    # gets returned with response to request
    primary_name = "Name not given"

    # user gets pulled out from id
    try:
        user = User.objects.get(id=user_id)
        company = Company.objects.get(id=company_id)
    except User.DoesNotExist or Company.DoesNotExist:
        raise Http404

    if not user.opt_in_employers:
        raise Http404

    urls = saved_searches(request.user, company, user)

    if not urls:
        raise Http404

    manager = PrimaryNameProfileUnitManager()
    models = manager.displayed_units(user.profileunits_set.all())

    try:
        primary_name = manager.primary_name
    except:
        pass

    if request.REQUEST.get('url'):
        microsite_url = request.REQUEST.get('url')
        coming_from = {'path': 'microsite', 'url': microsite_url}
    else:
        coming_from = {'path': 'view'}

    searches = user.savedsearch_set.filter(url__in=urls)

    data_dict = {'user_info': models,
                 'company_id': company_id,
                 'primary_name': primary_name,
                 'the_user': user,
                 'searches': searches,
                 'coming_from': coming_from}

    return render_to_response('mydashboard/candidate_information.html',
                              data_dict, RequestContext(request))
