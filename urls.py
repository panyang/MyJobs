from django.conf.urls import *
from django.contrib import admin

from tastypie.api import Api

from myjobs.api import UserResource, SavedSearchResource

admin.autodiscover()

# API Resources
v1_api = Api(api_name='v1')
v1_api.register(UserResource())
v1_api.register(SavedSearchResource())


urlpatterns = patterns('',
    url('', include('MyJobs.myjobs.urls')),
    url(r'^candidates/',
        include('MyJobs.mydashboard.urls')),
    url(r'^accounts/', include('MyJobs.registration.urls')),
    url(r'^profile/',
        include('MyJobs.myprofile.urls')),
    url(r'^saved-search/',
        include('MyJobs.mysearches.urls')),
    url(r'^api/', include(v1_api.urls)),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^authorize/', include('MyJobs.mysignon.urls')),
    url(r'^analytics/', include('MyJobs.myanalytics.urls')),
)
