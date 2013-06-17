from datetime import datetime, timedelta
import time
from urlparse import urlparse

from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render_to_response
from django.template import RequestContext

from myjobs.models import User
from mysearches.models import SavedSearch


@user_passes_test(lambda u: User.objects.is_group_member(u, 'Staff'))
def activity_search_feed(request):
    """
    Returns a list of users who created a saved search on the given microsite
    between the given (optional) dates
    """
    url = request.REQUEST.get('microsite')
    if url.find('//') == -1:
        url = '//' + url
    microsite = urlparse(url).netloc

    # saved search was created after this date...
    after = request.REQUEST.get('after')
    if after:
        after = datetime.strptime(after, '%Y-%m-%d')
    else:
        after = datetime.strptime('01/01/2013', '%d/%m/%Y')
    # ... and before this one
    before = request.REQUEST.get('before')
    if before:
        before = datetime.strptime(before, '%Y-%m-%d')
    else:
        before = datetime.now()

    # Prefetch the user (and its profileunits)
    searches = SavedSearch.objects.select_related('user', 'user__profileunits_set')

    # All searches saved from a given microsite
    searches = searches.filter(url__contains=microsite)

    # Specific microsite searches saved between two dates
    searches = searches.filter(created_on__range=[after, before])
    data = {'searches': searches, 'site': microsite}
    return render_to_response('myactivity/activity_feed.html', data,
                              RequestContext(request))
