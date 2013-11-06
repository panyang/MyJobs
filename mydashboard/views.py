import operator
import csv
import itertools

from datetime import datetime, timedelta
from collections import Counter

from django.contrib.auth.decorators import user_passes_test
from django.db.models import Q
from django.http import Http404, HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response

from mydashboard.helpers import saved_searches
from mydashboard.models import *
from myjobs.models import User
from myprofile.models import (PrimaryNameProfileUnitManager,
                              ProfileUnits)
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
        'candidates': SavedSearch.objects.all().exclude(
            user__opt_in_employers=False),
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
    candidates_page = request.REQUEST.get('page', 1)    
          
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
    try:
        candidate_searches = candidate_searches.filter(reduce(
            operator.or_, q_list)).filter(
                created_on__range=[after, before]).exclude(
                    user__opt_in_employers=False).order_by('-created_on')
    except:
        raise Http404
    
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
               'candidates_page': candidates_page,               
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
    context = {
        'candidates': SavedSearch.objects.all().exclude(
            user__opt_in_employers=False),
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
    candidates_page = request.REQUEST.get('page', 1)
    
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
        
    # Specific microsite searches saved between two dates
    candidate_searches = SavedSearch.objects.filter(
        created_on__range=[after, before]).filter(
            url__contains=requested_microsite).order_by('-created_on')
    
    saved_search_count = candidate_searches.count()      
    
    context = {'microsite_url': requested_microsite,
               'after': after,
               'before': before,
               'candidates': candidate_searches,
               'view_name': 'Company Dashboard',
               'company_name': company.name,
               'company_id': company.id,
               'date_button': requested_date_button,
               'candidates_page': candidates_page,
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
    anchor_id = request.REQUEST.get('anchor', False)
    after = request.REQUEST.get('after', False)
    before = request.REQUEST.get('before', False)    
    candidates_page = request.REQUEST.get('page', False)
    
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

    manager = PrimaryNameProfileUnitManager(order=['employmenthistory',
                                                   'education',
                                                   'militaryservice'])
    models = manager.displayed_units(user.profileunits_set.all())

    primary_name = getattr(manager, 'primary_name', 'Name not given')

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
                 'after': after,
                 'anchor': anchor_id,
                 'before': before,                 
                 'candidates_page': candidates_page,
                 'coming_from': coming_from}

    return render_to_response('mydashboard/candidate_information.html',
                              data_dict, RequestContext(request))


def filter_candidates(request):
    """
    Some default filtering for company/microsite. This function will
    be changing with solr docs update and filtering addition.
    """
    candidates = []
    company_id = request.REQUEST.get('company')
    try:
        company = Company.objects.get(id=company_id)
    except Company.DoesNotExist:
        raise Http404
    requested_microsite = request.REQUEST.get('microsite', company.name)
    authorized_microsites = Microsite.objects.filter(company=company.id)
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

    # Specific microsite searches saved between two dates
    candidate_searches = candidate_searches.filter(reduce(
        operator.or_, q_list)).exclude(
            user__opt_in_employers=False).order_by('-created_on')
    for search in candidate_searches:
        candidates.append(search.user)
    return set(candidates)


@user_passes_test(lambda u: User.objects.is_group_member(u, 'Employer'))
def export_candidates(request):
    """
    This function will be handling which export type to execute.
    Only function accessible through url.
    """
    try:
        if request.GET['ex-t'] == 'csv':
            candidates = filter_candidates(request)
            response = export_csv(request, candidates)
    except:
        raise Http404
    return response


def export_csv(request, candidates, models_excluded=[], fields_excluded=[]):
    """
    Exports comma-separated values file. Function is seperated into two parts:
    creation of the header, creating user data.

    Header creation uses a tuple and a Counter to determine the max amount
    of each module type (education, employmenthistory, etc). Then the header
    is created in the format of [model]_[field_name]_[count] excluding models
    and or fields in either lists (models_excluded and fields_excluded). The
    header is always the first line in the csv.

    User data creation iterates through the list of candidates and references
    the header to determine what model and field to use getattr. Each user has
    their own line in the csv.

    Inputs:
    :candidates:        A set list of Users
    :models_excluded:   List of strings that represents profileunits
                        content_type model names
    :fields_excluded:   List of strings that would target specific fields

    Outputs:
    :response:          Sends a .csv file to the user.
    """
    response = HttpResponse(mimetype='text/csv')
    time = datetime.now().strftime('%m%d%Y')
    company_id = request.REQUEST.get('company')
    try:
        company = Company.objects.get(id=company_id)
    except Company.DoesNotExist:
        raise Http404
    response['Content-Disposition'] = ('attachment; filename=' +
                                       company.name+"_DE_"+time+'.csv')
    writer = csv.writer(response)

    users_units = ProfileUnits.objects.filter(
        user__in=candidates).select_related('user__id', 'content_type__name')

    # Creating header for CSV
    headers = ["primary_email"]
    models = [model for model in
              ProfileUnits.__subclasses__() if model._meta.module_name
              not in models_excluded]

    tup = [(x.user.id, x.content_type.name) for x in users_units]
    tup_counter = Counter(tup)
    final_count = {}
    module_names = [x._meta.module_name for x in models]
    tup_most_common = tup_counter.most_common()
    for module_name in module_names:
        for counted_model in tup_most_common:
            if (counted_model[0][1].replace(" ", "") == unicode(module_name)
                    and counted_model[0][1].replace(" ", "")
                    not in final_count):
                final_count[module_name] = counted_model[1]
    for model in models:
        module_count = 0
        current_count = 1
        if model._meta.module_name in final_count:
            module_count = final_count[model._meta.module_name]
        while current_count <= module_count:
            models_with_fields = []
            fields = [field for field in
                      model._meta.get_all_field_names() if unicode(field) not
                      in [u'id', u'user', u'profileunits_ptr', u'date_created',
                      u'date_updated', u'content_type']]
            for field in fields:
                if field not in fields_excluded:
                    ufield = model._meta.module_name + "_" + field + "_" + str(
                        current_count)
                else:
                    continue
                if ufield:
                    models_with_fields.append(ufield)
            headers.extend(models_with_fields)
            current_count += 1
    writer.writerow(headers)

    # Making user info rows
    for user in candidates:
        grouped_units = {}
        user_fields = [user.email]
        units = users_units.filter(user=user)
        for k, v in itertools.groupby(units, lambda x: x.content_type.name):
            grouped_units[k.replace(" ", "")] = list(v)
        if units:
            for header in headers[1:]:
                header_split = header.split('_')
                model = header_split[0]
                num = header_split[-1]
                field = "_".join(header_split[1:-1])
                if model in grouped_units:
                    try:
                        pu_instance = grouped_units[model][int(num)-1]
                        instance = getattr(
                            pu_instance, pu_instance.content_type.name.replace(
                                " ", ""))
                    except IndexError:
                        instance = None

                value = getattr(instance, field, u'')
                value = unicode(value).encode('utf8')
                user_fields.append('"%s"' % value.replace('\r\n', ''))
        else:
            for header in headers[1:]:
                user_fields.append('""')
        writer.writerow(user_fields)

    return response

