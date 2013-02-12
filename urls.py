from django.conf.urls.defaults import *
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url('', include('MyJobs.myjobs.urls')),
    url(r'^accounts/', include('MyJobs.registration.urls')),
    url(r'', include('MyJobs.mysearches.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
