from django.conf.urls.defaults import patterns, url, include
from django.http import HttpResponsePermanentRedirect

urlpatterns = patterns('MyJobs.mymessages.views',
    url(r'^messages/$', 'messages', name='messages'),
    url(r'^message/new$', 'new_message', name='new_message'),
    url(r'^message/(?P<mail_id>)/$', 'read_message', name='read_message'),
    url(r'^message/(?P<mail_id>)/delete$', 'delete_message', 
        name='delete_message')
)
