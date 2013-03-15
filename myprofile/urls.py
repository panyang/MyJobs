from django.conf.urls.defaults import patterns, url, include
from django.contrib import admin
from django.http import HttpResponsePermanentRedirect

from myjobs.views import *

urlpatterns = patterns('MyJobs.myprofile.views',
    url(r'^edit/$', 'edit_profile', name='edit_profile'),
)
