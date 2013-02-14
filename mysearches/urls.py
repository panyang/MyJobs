from django.conf.urls.defaults import *

from mysearches.views import *

# Authorization URLS
urlpatterns = patterns('',
    url(r'^saved-search/edit$', saved_search_form, name='saved_search_form'),
    url(r'^saved-search/$', saved_search_main, name='saved_search_main'),
)

