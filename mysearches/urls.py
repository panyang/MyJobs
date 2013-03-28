from django.conf.urls.defaults import *

from mysearches.views import *

# Authorization URLS
urlpatterns = patterns('',
    url(r'^edit/(?P<search_id>\d+)/$', edit_saved_search, name='edit_saved_search'),
    url(r'^delete/(?P<search_id>\d+)/$', delete_saved_search, name='delete_saved_search'),
    url(r'^$', saved_search_main, name='saved_search_main'),
    url(r'^(?P<search_id>\d+)/$', view_full_feed, name='view_full_feed'),
    url(r'^more-results$', more_feed_results, name='more_feed_results'),
)
