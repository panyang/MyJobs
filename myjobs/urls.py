from django.conf.urls.defaults import patterns, url, include
from django.contrib import admin
from django.http import HttpResponsePermanentRedirect
from django.views.generic import RedirectView

from myjobs.views import *

urlpatterns = patterns('MyJobs.myjobs.views',
    url(r'^$', 'home', name='home'),
    url(r'^about/$', About.as_view(), name='about'),
    url(r'^privacy/$', Privacy.as_view(), name='privacy'),
    url(r'^terms/$', Terms.as_view(), name='terms'),
    url(r'^contact/$', 'contact', name='contact'),
    url(r'^account/$', 'edit_account', name='edit_account'),
    url(r'^account/delete$', 'delete_account', name='delete_account'),
    url(r'^account/disable$', 'disable_account', name='disable_account'),
    url(r'^account/edit$', RedirectView.as_view(url='/account/')),
    url(r'^edit/basic$', 'edit_basic', name='edit_basic'),
    url(r'^edit/password$', 'edit_password', name='edit_password'),
    url(r'^edit/delete$', 'edit_delete', name='edit_delete'),
    url(r'^edit/disable$', 'edit_disable', name='edit_disable'),
    url(r'^edit/communication$', 'edit_communication', name='edit_communication'),
    url(r'^error/$', 'error', name='error'),
    url(r'^batch$', 'batch_message_digest', name='batch_message_digest'),
    url(r'^send/$', 'continue_sending_mail', name='continue_sending_mail'),
    url(r'^success/$', Success.as_view(), name='success')
)
