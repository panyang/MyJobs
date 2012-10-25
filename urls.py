from django.conf.urls.defaults import patterns, url, include
from django.contrib import admin
from django.http import HttpResponsePermanentRedirect
#admin.autodiscover()

urlpatterns = patterns('',
    url('', include('MyJobs.app.urls')),
    url(r'^accounts/', include('MyJobs.registration.urls')),
#    url(r'^admin/', include(admin.site.urls)),
    # social_auth urls
#    url(r'', include('social_auth.urls')),
)
