from django.conf.urls.defaults import patterns, url


urlpatterns = patterns('MyJobs.mydashboard.views',
    url(r'^$', 'dashboard', name='dashboard'),
    url(r'^view$', 'dashboard', name='dashboard'),
    url(r'^view/details$', 'candidate_information',
        name='candidate_information'),
    url(r'^view/microsite$', 'microsite_activity', name='microsite_activity'),
)
