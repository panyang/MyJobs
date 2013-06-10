from django.conf.urls.defaults import *

from mysearches.views import *

# Authorization URLS
urlpatterns = patterns('',
    url(r'^delete/(?P<search_id>\d+)/$', delete_saved_search, name='delete_saved_search'),
    url(r'^$', saved_search_main, name='saved_search_main'),
    url(r'^more-results/$', more_feed_results, name='more_feed_results'),
    url(r'^(?P<search_id>\d+)/$', view_full_feed, name='view_full_feed'),
    url(r'^validate-url$', validate_url, name='validate_url'),
    url(r'^save-digest$', save_digest_form, name='save_digest_form'),
    url(r'^edit$', get_edit_template, name='get_edit_template'),
    url(r'^save$', save_search_form, name='save_search_form'),
    url(r'^digest-unsub/(?P<digest_id>\d+)/$', digest_unsubscribe, name='digest_unsubscribe'),
    url(r'^search-unsub/(?P<search_id>\d+)/$', search_unsubscribe, name='search_unsubscribe'),
)
