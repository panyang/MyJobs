from django.conf.urls.defaults import patterns, url

from myactivity.views import *

urlpatterns = patterns('MyJobs.myactivity.views',
    url(r'^$', 'activity_search_feed', name='activity_search_feed'),
    url(r'^(?P<user_id>\d+)/?$', 'candidate_information', name='candidate_information'),
)
