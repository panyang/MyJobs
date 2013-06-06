from django.conf.urls.defaults import patterns, url, include
from django.contrib import admin
from django.http import HttpResponsePermanentRedirect

from myjobs.views import *

urlpatterns = patterns('MyJobs.myprofile.views',
    url(r'^$', 'edit_profile', name='view_profile'),
    url(r'^edit/$', 'edit_profile', name='edit_profile'),
    url(r'^delete/$', 'delete_item', name='delete_item'),
    url(r'^form/$', 'handle_form', name='handle_form'),
    url(r'^details/$', 'get_details', name='get_details'),
)
