import json
from datetime import datetime
from itertools import chain

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404

from mysearches.models import SavedSearch, SavedSearchDigest
from mysearches.forms import SavedSearchForm, DigestForm
from mysearches.helpers import *

@login_required
def add_saved_search(request):
    if request.method == "POST":
        form = SavedSearchForm(user=request.user, data=request.POST)
        if request.POST.get('action', None) == 'validate' :
            rss_url, rss_soup = validate_dotjobs_url(request.POST['url'])
            if rss_url:
               feed_title = get_feed_title(rss_soup)
               # returns the RSS url via AJAX to show if field is validated
               # id valid, the label field is auto populated with the feed_title
               data = {'rss_url': rss_url,
                       'feed_title': feed_title,
                       'url_status': 'valid'
               }
            else:
                data = {'url_status': 'not valid'}
            return HttpResponse(json.dumps(data))
        else:
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/saved-search')
    else:
        form = SavedSearchForm(user=request.user)
        
    return render_to_response('mysearches/saved_search_form.html',
                              {'form':form},
                              RequestContext(request))

@login_required
def edit_saved_search(request, search_id):
    saved_search = SavedSearch.objects.get(id=search_id)
    if request.user == saved_search.user:
        if request.method == "POST":
            form = SavedSearchForm(user=request.user, data=request.POST,
                                   instance=saved_search)
            
            if request.POST.get('action', None) == 'validate' :
                rss_url,rss_soup = validate_dotjobs_url(request.POST['url'])
                if rss_url:
                    feed_title = get_feed_title(rss_soup)
                    data = {'rss_url': rss_url,
                            'feed_title': feed_title,
                            'url_status': 'valid'
                        }
                else:
                    data = {'url_status': 'not valid'}
                return HttpResponse(json.dumps(data))
            else:
                if form.is_valid():
                    form.save()
                    return HttpResponseRedirect('/saved-search')
        else:
            form = SavedSearchForm(user=request.user, instance=saved_search)
        return render_to_response('mysearches/saved_search_edit.html',
                                  {'form':form, 'search_id':search_id},
                                  RequestContext(request))

@login_required
def delete_saved_search(request,search_id):
    saved_search = SavedSearch.objects.get(id=search_id)
    if request.user == saved_search.user:
        saved_search.delete()
    return  HttpResponseRedirect('/saved-search')
        
@login_required
def saved_search_main(request):
    # instantiate the form if the digest object exists
    try:
        digest_obj = SavedSearchDigest.objects.get(user=request.user)
    except:
        digest_obj = None
    saved_searches = SavedSearch.objects.filter(user=request.user)
    if request.method == "POST":
        form = DigestForm(user=request.user, data=request.POST,
                          instance=digest_obj)
        if form.is_valid():
            form.save()
            data = "success"
        else:
            data = "failure"
        if request.POST.get('action') == 'save':
            return HttpResponse(data)
    else:
        form = DigestForm(user=request.user, instance=digest_obj)
    return render_to_response('mysearches/saved_search_main.html',
                              {'saved_searches': saved_searches,
                               'form':form},
                              RequestContext(request))

@login_required
def view_full_feed(request, search_id):
    saved_search = SavedSearch.objects.get(id=search_id)
    if request.user == saved_search.user:
        items = parse_rss(saved_search.feed, saved_search.frequency)
        date = datetime.date.today()
        label = saved_search.label
        return render_to_response('mysearches/view_full_feed.html',
                                  {'label': label,
                                   'feed': saved_search.feed,
                                   'frequency': saved_search.frequency,
                                   'verbose_frequency': saved_search.get_verbose_frequency(),
                                   'link': saved_search.url,
                                   'items': items},
                                  RequestContext(request))
    else:
        return HttpResponseRedirect('/saved-search')

def more_feed_results(request):
    # Ajax request comes from the view_full_feed view when user scrolls to bottom
    # of the page
    if request.is_ajax():
        items = parse_rss(request.GET['feed'], request.GET['frequency'],
                          offset=request.GET['offset'])
        return render_to_response('mysearches/feed_page.html',
                                  {'items':items}, RequestContext(request))
