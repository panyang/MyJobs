from django.conf.urls import *
from django.views.generic import RedirectView

from mysearches.views import *

# Authorization URLS
urlpatterns = patterns('',
    url(r'^view/delete$', delete_saved_search, name='delete_saved_search'),
    url(r'^$', RedirectView.as_view(url='/saved-search/view/')),
    url(r'^view/$', saved_search_main, name='saved_search_main'),
    url(r'^view/feed$', view_full_feed, name='view_full_feed'),
    url(r'^view/more-results/$', more_feed_results, name='more_feed_results'),
    url(r'^view/validate-url/$', validate_url, name='validate_url'),
    url(r'^view/save-digest/$', save_digest_form, name='save_digest_form'),
    url(r'^view/edit/$', edit_search, name='edit_search'),
    url(r'^view/edit$', edit_search, name='edit_search'),
    url(r'^view/save/$', save_search_form, name='save_search_form'),
    url(r'^view/unsubscribe$', unsubscribe, name='unsubscribe'),
)
