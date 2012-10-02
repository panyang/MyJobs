from django.conf.urls.defaults import patterns, url, include
from django.contrib import admin
from django.http import HttpResponsePermanentRedirect
from app.views import *
admin.autodiscover()

urlpatterns = patterns('',
    url('', include('MyJobs.app.urls', namespace='myjobs',
                    app_name='app')),
    url(r'^admin/', include(admin.site.urls)),
    # social_auth urls
    url(r'', include('social_auth.urls')),
    # django_registration urls
    (r'^accounts/', include('registration.urls')),
)
