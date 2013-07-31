from django.conf.urls.defaults import *

from mysearches.views import *

# Authorization URLS
urlpatterns = patterns('',
    url(r'^delete/(?P<user_email>(\S+))/(?P<search_id>(\d+|digest))/$', delete_saved_search, name='delete_saved_search'),
    url(r'^$', saved_search_main, name='saved_search_main'),
    url(r'^more-results/$', more_feed_results, name='more_feed_results'),
    url(r'^(?P<search_id>\d+)/$', view_full_feed, name='view_full_feed'),
    url(r'^validate-url/$', validate_url, name='validate_url'),
    url(r'^save-digest/$', save_digest_form, name='save_digest_form'),
    url(r'^edit/$', edit_search , name='edit_search'),
    url(r'^edit/(?P<search_id>\d+)/$', edit_search, name='edit_search'),
    url(r'^save/$', save_search_form, name='save_search_form'),
    url(r'^unsubscribe/(?P<user_email>(\S+))/(?P<search_id>(\d+|digest))/$', unsubscribe, name='unsubscribe'),
)
