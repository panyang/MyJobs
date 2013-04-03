from django.conf.urls.defaults import *

from mysearches.views import *

# Authorization URLS
urlpatterns = patterns('',
    url(r'^delete/(?P<search_id>\d+)/$', delete_saved_search, name='delete_saved_search'),
    url(r'^$', saved_search_main, name='saved_search_main'),
    url(r'^(?P<search_id>\d+)/$', view_full_feed, name='view_full_feed'),
    url(r'^validate-url$', validate_url, name='validate_url'),
    url(r'^save-digest$', save_digest_form, name='save_digest_form'),
    url(r'^delete-digest$', delete_digest_form, name='delete_digest_form'),
    url(r'^new$', save_new_search_form, name='save_new_search_form'),
    url(r'^edit$', get_edit_template, name='get_edit_template'),
    url(r'^save-edit$', save_edit_form, name='save_edit_form'),
)
