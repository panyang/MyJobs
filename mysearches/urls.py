from django.conf.urls.defaults import *

from mysearches.views import *

# Authorization URLS
urlpatterns = patterns('',
                       url(r'^saved-search/$',
                           save_search_form,
                           name='saved_search_form'),
)

