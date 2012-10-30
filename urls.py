from django.conf.urls.defaults import *
from django.contrib import admin
#admin.autodiscover()

urlpatterns = patterns('',
    url('', include('MyJobs.app.urls')),
    url(r'^accounts/', include('MyJobs.registration.urls')),
#    url(r'^admin/', include(admin.site.urls)),
#    url(r'', include('social_auth.urls')),
)
