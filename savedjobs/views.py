import requests

from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404

from secrets import SEO_USER, SEO_KEY
from savedjobs.models import *
from savedjobs.forms import *

@login_required
def microsite_job_save(request):
    """
    Takes the unique job id parsed using the save job javascript widget and
    collects the job information from the DirectSEO Api. The result is then
    saved to the database and linked to the SavedJob model.

    :Input:
    (Parameters in request.GET)
    uid - Unique job id collected from microsite URL
    source - URL from which the job was saved.
    """
    
    uid = request.GET.get('uid')
    source= request.GET.get('source')
    
    params = {'format': 'json',
              'username': SEO_USER,
              'api_key': SEO_KEY}
    resource_uri = 'http://jobs.directemployers.org/api/v1/jobsearch/%s/' % uid
    job_object = requests.get(resource_uri, params=params).json

    # Check if job exists
    if job_object['uid']:
        if not SavedJob.objects.filter(url=source):
            SavedJob.objects.create(user=request.user,
                                    url = source,
                                    uid=uid,
                                    title=job_object['title'],
                                    company=job_object['company'],
                                    city=job_object['city'],
                                    state=job_object['state'],
                                    country=job_object['country'],
                                    onet=job_object['onet'],
                                    from_microsite=True)
            # We'll want the javascript interfacing this view to display these
            # HTTP responses for user validation
            return HttpResponse('Success')
        else:
            return HttpResponse('Job already exists!')
    else:
        return HttpResponse('Job Not Found')

@login_required
def manual_job_save(request):
    """
    There is only one saved job view. All options are handled through ajax requests.
    The POST received from an AJAX call contains a special flag, 'action', to
    differentiate between adds, deletes, and edits. After an ajax request, this
    view renders saved_job.html, which is just a single saved job to be appended or
    updated on the page.
    
    """
    saved_jobs = SavedJob.objects.filter(user=request.user).order_by('-date_saved')
    if request.method == "POST":
        form = SaveJobForm(request.POST)
        if request.is_ajax():
            if request.POST['action'] == "delete":
                SavedJob.objects.get(id=request.POST['id']).delete()
            if form.is_valid():
                if request.POST['action'] == "add":
                    saved_job = form.save(request.user)
                if request.POST['action'] == "edit":
                    saved_job = form.edit(request.user)
                return render_to_response('savedjobs/saved_job.html',
                                          {'saved_job': saved_job, 'form':form},
                                          context_instance=RequestContext(request))
    else:
        form = SaveJobForm()
    return render_to_response('savedjobs/saved_jobs_main.html',
                              {'form':form, 'saved_jobs': saved_jobs},
                              context_instance=RequestContext(request))
