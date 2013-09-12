from django.conf.urls import patterns, url


urlpatterns = patterns('MyJobs.mysignon.views',
    url(r'^$', 'sso_authorize', name='sso_authorize'),
)
