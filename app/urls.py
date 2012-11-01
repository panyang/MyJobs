from django.conf.urls.defaults import patterns, url, include
from django.contrib import admin
from django.http import HttpResponsePermanentRedirect
from app.views import *

urlpatterns = patterns('MyJobs.app.views',
    #url(r'^$', lambda request: HttpResponsePermanentRedirect('http://jobs.jobs')),
    url(r'^$', 'home', name='home'),
    url(r'^about/$', About.as_view()),
    url(r'^auth/(?P<provider>[\w]+?)/$', 'auth_popup'),
    url(r'^privacy/$', Privacy.as_view()),
    url(r'^profile/$', 'user_view_profile', name='profile'),
    url(r'^done/$', 'done', name='done'),
    url(r'^error/$', 'error', name='error'),
#    url(r'^share/(?P<provider>[\w]+?)$', 'share', name='share'),
    url(r'^redirect/$', 'login_redirect', name='login_redirect'),
    url(r'^remove/(?P<provider>[\w]+?)$', 'remove_association',
        name='remove_association')
)
