from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404

from mysearches.forms import SavedSearchForm

@login_required
def save_search_form(request):
    form = SavedSearchForm(user=request.user)
    return render_to_response('mysearches/saved_search_form.html',
                              {'form':form}, RequestContext(request))
