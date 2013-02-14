import json

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404

from mysearches.forms import SavedSearchForm
from mysearches.helpers import validate_search_url,get_feed_title

@login_required
def save_search_form(request):
    if request.method == "POST":
        form = SavedSearchForm(user=request.user, data=request.POST)
        if request.POST['action'] == "validate":
            rss_url = validate_search_url(request.POST['url'])
            if rss_url:
               feed_title = get_feed_title(rss_url)
               data = {'rss_url': rss_url,
                       'feed_title': feed_title,
                       'url_status': 'valid'
               }
            else:
                data = {'url_status': 'not valid'}
            return HttpResponse(json.dumps(data))
    else:
        form = SavedSearchForm(user=request.user)
        
    return render_to_response('mysearches/saved_search_form.html',
                              {'form':form}, RequestContext(request))
