import json
from datetime import datetime
from itertools import chain

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext, loader
from django.shortcuts import render_to_response, get_object_or_404

from myjobs.models import User
from mysearches.models import SavedSearch, SavedSearchDigest
from mysearches.forms import SavedSearchForm, DigestForm
from mysearches.helpers import *

@user_passes_test(User.objects.is_active)
@user_passes_test(User.objects.not_disabled)
def delete_saved_search(request,search_id):
    try:
        search_id = int(search_id)
        SavedSearch.objects.get(id=search_id, user=request.user).delete()
    except SavedSearch.DoesNotExist:
        pass
    except ValueError:
        SavedSearch.objects.filter(user=request.user).delete()
    return  HttpResponseRedirect('/saved-search')
        
@user_passes_test(User.objects.is_active)
@user_passes_test(User.objects.not_disabled)
def saved_search_main(request):
    # instantiate the form if the digest object exists
    try:
        digest_obj = SavedSearchDigest.objects.get(user=request.user)
    except:
        digest_obj = None
    saved_searches = SavedSearch.objects.filter(user=request.user)
    form = DigestForm(user=request.user, instance=digest_obj)
    add_form = SavedSearchForm(user=request.user)
    return render_to_response('mysearches/saved_search_main.html',
                              {'saved_searches': saved_searches,
                               'form':form, 'add_form': add_form},
                              RequestContext(request))

@user_passes_test(User.objects.is_active)
@user_passes_test(User.objects.not_disabled)
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
                                   'verbose_frequency':
                                     saved_search.get_verbose_frequency(),
                                   'link': saved_search.url,
                                   'items': items},
                                  RequestContext(request))
    else:
        return HttpResponseRedirect('/saved-search')

@user_passes_test(User.objects.is_active)
@user_passes_test(User.objects.not_disabled)
def more_feed_results(request):
    # Ajax request comes from the view_full_feed view when user scrolls to
    # bottom of the page
    if request.is_ajax():
        items = parse_rss(request.GET['feed'], request.GET['frequency'],
                          offset=request.GET['offset'])
        return render_to_response('mysearches/feed_page.html',
                                  {'items':items}, RequestContext(request))

@user_passes_test(User.objects.is_active)
@user_passes_test(User.objects.not_disabled)
def validate_url(request):
    if request.is_ajax():
        feed_title, rss_url = validate_dotjobs_url(request.POST['url'])
        if rss_url:
           # returns the RSS url via AJAX to show if field is validated
           # id valid, the label field is auto populated with the feed_title
           data = {'rss_url': rss_url,
                   'feed_title': feed_title,
                   'url_status': 'valid'}

        else:
            data = {'url_status': 'not valid'}
        return HttpResponse(json.dumps(data))

@user_passes_test(User.objects.is_active)
@user_passes_test(User.objects.not_disabled)
def save_digest_form(request):
    if request.is_ajax():
        try:
            digest_obj = SavedSearchDigest.objects.get(user=request.user)
        except:
            digest_obj = None
        form = DigestForm(user=request.user, data=request.POST,
                          instance=digest_obj)
        if form.is_valid():
            form.save()
            data = "success"
        else:
            data = "failure"
        return HttpResponse(data)

@user_passes_test(User.objects.is_active)
@user_passes_test(User.objects.not_disabled)
def save_new_search_form(request):
    if request.is_ajax():
        add_form = SavedSearchForm(user=request.user, data=request.POST)
        if add_form.is_valid():
            add_form.save()
            return HttpResponse('success')
        else:
            return HttpResponse(json.dumps(add_form.errors))

@user_passes_test(User.objects.is_active)
@user_passes_test(User.objects.not_disabled)
def get_edit_template(request):
    if request.is_ajax():
        search_id = request.POST.get('search_id')
        try:
            saved_search = SavedSearch.objects.get(id=search_id)
        except SavedSearch.DoesNotExist:
            saved_search = None
        form = SavedSearchForm(user=request.user, instance=saved_search,
                               auto_id='id_edit_%s')
        return render_to_response('mysearches/saved_search_edit.html',
                                  {'form':form, 'search_id':search_id},
                                  RequestContext(request))

@user_passes_test(User.objects.is_active)
@user_passes_test(User.objects.not_disabled)
def save_edit_form(request):
    if request.is_ajax():
        search_id = request.POST.get('search_id')
        saved_search = SavedSearch.objects.get(id=search_id)
        if request.user == saved_search.user:
            form = SavedSearchForm(user=request.user, data=request.POST,
                                   instance=saved_search)
            if form.is_valid():
                form.save()
                return HttpResponse('success')
            else:
                return HttpResponse(json.dumps(form.errors))

@user_passes_test(User.objects.is_active)
@user_passes_test(User.objects.not_disabled)
def unsubscribe(request, search_id):
    try:
        search_id = int(search_id)
        # a single search is being deactivated
        saved_search = SavedSearch.objects.filter(id=search_id, user=request.user)
        saved_search.update(is_active=False)
    except ValueError:
        # a digest is being deactivated
        digests = SavedSearchDigest.objects.filter(user=request.user,
                                                 is_active=True)
        if digests.count() == 1:
            digests.update(is_active=False)
            saved_search = SavedSearch.objects.filter(user=request.user)
            saved_search.update(is_active=False)
        else:
            saved_search = []
    return render_to_response('mysearches/saved_search_disable.html',
                              {'search_id': search_id, 'searches': saved_search},
                              RequestContext(request))
