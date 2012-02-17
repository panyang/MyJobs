from django.conf.urls.defaults import patterns, url, include
from django.contrib import admin
from django.http import HttpResponsePermanentRedirect
from app.views import home, done, logout, error, about, privacy, password_connection, profile, coming_soon, user_view_profile


admin.autodiscover()

urlpatterns = patterns('',
    # url(r'^$', lambda request: HttpResponsePermanentRedirect('http://jobs.jobs')),
    url(r'^$', home, name='home'),
    url(r'^home/$', home, name='home'),
    url(r'^profile/$', user_view_profile, name='user_view_profile'), 
    url(r'^profle/(?P<username>\w+)/$', profile, name='profile'),
    url(r'^about/$', about, name='about'),
    url(r'^privacy/$', privacy, name='privacy'),     
    url(r'^done/$', done, name='done'),
    url(r'^error/$', error, name='error'),
    url(r'^logout/$', logout, name='logout'),
    url(r'^lost_password/$', password_connection, name='lost_password'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^coming_soon', coming_soon, name='comingsoon'),
    # social_auth urls
    url(r'', include('social_auth.urls')),
    # django_registration urls
    (r'^profile/', include('registration.urls')),
)
