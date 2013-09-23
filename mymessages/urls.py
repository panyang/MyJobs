from django.conf.urls import patterns, url
from django.views.generic import RedirectView

urlpatterns = patterns('MyJobs.mymessages.views',
    url(r'^$', 'read', name='read'),
)