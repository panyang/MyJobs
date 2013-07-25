from datetime import datetime, timedelta
import time
from urlparse import urlparse

from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.db import models
from django.http import Http404

from myjobs.models import User
from mysearches.models import SavedSearch
from myprofile.models import ProfileUnits
from mydashboard.models import Company
from myactivity.helpers import *

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
    """
    Sends user info, primary name, and searches to candidate_information.html.
    Gathers the employer's (request.user) companies and microsites and puts 
    the microsites' domains in a list for further checking and logic, 
    see helpers.py.
    """
    # gets returned with response to request
    data_dict = {}
    models = {}
    name = "Name not given"

    # user gets pulled out from id
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        raise Http404

    url_list = saved_seaches(request.user, user)
    if not url_list:
        raise Http404

    if not user.opt_in_employers:
        raise Http404

    units = ProfileUnits.objects.filter(user=user)

    for unit in units:
        if unit.__getattribute__(unit.get_model_name()).is_displayed():
            models.setdefault(unit.get_model_name(), []).append(
            unit.__getattribute__(unit.get_model_name()))

    # if Name ProfileUnit exsists
    if models.get('name'):
        name=models['name'][0]
        del models['name']

    searches = user.savedsearch_set.filter(url__in=url_list)

    data_dict = {'user_info': models,
                'primary_name': name,
                'the_user': user,
                'searches': searches}

    return render_to_response('myactivity/candidate_information.html', data_dict,
                            RequestContext(request))
