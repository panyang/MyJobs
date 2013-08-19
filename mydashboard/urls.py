from django.conf.urls.defaults import patterns, url


urlpatterns = patterns('MyJobs.mydashboard.views',
    url(r'^view$', 'dashboard', name='dashboard'),
    url(r'^view/candidate$', 'candidate_information',
        name='view_candidate_information'),
    url(r'^microsite$', 'microsite_activity', name='microsite_activity'),
    url(r'^microsite/candidate$', 'candidate_information',
        name='microsite_candidate_information'),
)
