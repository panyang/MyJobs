from django.conf.urls.defaults import patterns, url, include
from django.contrib import admin
from django.http import HttpResponsePermanentRedirect

from myjobs.views import *

urlpatterns = patterns('MyJobs.savedjobs.views',
    url(r'^save/microsite/$', 'microsite_job_save', name='microsite_job_save'),
    url(r'^save/job/$', 'manual_job_save', name='manual_job_save'),
)
