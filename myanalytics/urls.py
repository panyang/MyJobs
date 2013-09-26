from django.conf.urls import url, patterns


urlpatterns = patterns('MyJobs.myanalytics.views',
    url(r'^track$', 'track', name='track'),
)
