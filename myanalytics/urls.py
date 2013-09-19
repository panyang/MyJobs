from django.conf.urls import url, patterns


urlpatterns = patterns('MyJobs.myanalytics.views',
    url('track/', 'track', name='track'),
    url('track/pixel.png', 'track_pixel', name='track_pixel'),
)
