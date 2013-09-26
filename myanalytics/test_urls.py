from django.conf.urls import url, patterns, include
from django.conf import settings

from MyJobs import urls
from myanalytics.test_views import test_view


urlpatterns = patterns('',
    url(r'^test$', test_view, name='analytics_test'),
    url(r'', include(urls)),
)