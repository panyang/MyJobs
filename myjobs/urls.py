from django.conf.urls.defaults import patterns, url, include
from django.contrib import admin
from django.http import HttpResponsePermanentRedirect

from myjobs.views import *

urlpatterns = patterns('MyJobs.myjobs.views',
    url(r'^$', 'home', name='home'),
    url(r'^about/$', About.as_view(), name='about'),
    url(r'^privacy/$', Privacy.as_view()),
    url(r'^account/$', 'view_account', name='view_account'),
    url(r'^edit/$', 'edit_account', name='edit_account'),
    url(r'^change-password/$', 'change_password', name='change_password'),
    url(r'^error/$', 'error', name='error'),
)
