from django.conf.urls.defaults import patterns, url, include
from django.contrib import admin
from django.http import HttpResponsePermanentRedirect

from myjobs.views import *

urlpatterns = patterns('MyJobs.mydashboard.views',
    url(r'^$', 'dashboard', name='dashboard'),
    url(r'^(?P<user_id>\d+)/?$', 'candidate_information', name='candidate_information'),    
)

