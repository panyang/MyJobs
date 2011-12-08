from django.conf.urls.defaults import patterns, url, include
from django.contrib import admin
from django.http import HttpResponsePermanentRedirect
from app.views import home, done, logout, error, about, privacy, password_connection


admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', lambda request: HttpResponsePermanentRedirect('http://jobs.jobs')),
    url(r'^home/$', home, name='home'),
    url(r'^about/$', about, name='about'),
    url(r'^privacy/$', privacy, name='privacy'),     
    url(r'^done/$', done, name='done'),
    url(r'^error/$', error, name='error'),
    url(r'^logout/$', logout, name='logout'),
    url(r'^lp/$', password_connection, name='lostpassword'),
    url(r'^admin/', include(admin.site.urls)),
    # social_auth urls
    url(r'', include('social_auth.urls')),
    # django_registration urls
    (r'^profile/', include('registration.urls')),
)
