from datetime import datetime, timedelta
import time
from urlparse import urlparse

from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.db import models

from myjobs.models import User
from mysearches.models import SavedSearch
from myprofile.models import ProfileUnits, Name, Education, Address, Telephone, EmploymentHistory, SecondaryEmail

@user_passes_test(lambda u: User.objects.is_group_member(u, 'Employer'))
def activity_search_feed(request):
    """
    Returns a list of users who created a saved search on the given microsite
    between the given (optional) dates
    """
    data = {}
    if request.method == 'POST':
        url = request.REQUEST.get('microsite')
        if url:
            if url.find('//') == -1:
                url = '//' + url
            microsite = urlparse(url).netloc
        else:
            microsite = 'indiana.jobs'
        data['site'] = microsite

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
        data['after'] = after
        data['before'] = before

        # Prefetch the user
        searches = SavedSearch.objects.select_related('user')

        # All searches saved from a given microsite
        searches = searches.filter(url__contains=microsite)

        # Specific microsite searches saved between two dates
        searches = searches.filter(created_on__range=[after, before])
        data['searches'] = searches
    return render_to_response('myactivity/activity_feed.html', data,
                              RequestContext(request))

@user_passes_test(lambda u: User.objects.is_group_member(u, 'Employer'))
def candidate_information(request, user_id):
    # gets returned with response to request
    data_dict = {}
    profile_config = []


    # user gets pulled out from id
    user = User.objects.get(id=user_id)
    units = request.user.profileunits_set

    # if there is a new profile module please add here
    module_list = ['Name', 'Education', 'EmploymentHistory', 'SecondaryEmail',
                   'Telephone', 'Address']
    
    units = user.profileunits_set
    for module in module_list:
        model = globals()[module]
        verbose = model._meta.verbose_name
            
        # holder list
        x= []

        module_config = {}
        module_units = units.filter(content_type__name=verbose)

        # Verbose is used nicely for headings or titles on front-end
        module_config['verbose'] = verbose.title()

        # Name can be used for id names in html due to no whitespace
        module_config['name'] = module
        for unit in module_units:
            if hasattr(unit, module.lower()):
                x.append(getattr(unit, module.lower()))
                    
        module_config['items'] = x

        profile_config.append(module_config)

    data_dict = {'userInfo': profile_config,
                 'theUser': user}
    return render_to_response('myactivity/candidate_information.html', data_dict,
                            RequestContext(request))
