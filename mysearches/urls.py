from django.conf.urls.defaults import *

from mysearches.views import *

# Authorization URLS
urlpatterns = patterns('',
    url(r'^add$', saved_search_form, name='saved_search_form'),
    url(r'^$', saved_search_main, name='saved_search_main'),
    url(r'^(?P<search_id>\d+)/$', view_full_feed, name='view_full_feed'),
)

