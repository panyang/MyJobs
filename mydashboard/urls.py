from django.conf.urls import patterns, url
from django.views.generic import RedirectView


urlpatterns = patterns('MyJobs.mydashboard.views',
    url(r'^$', RedirectView.as_view(url='/candidates/view/')),
    url(r'^view/$', 'dashboard', name='dashboard'),
    url(r'^view$', 'dashboard', name='dashboard'),
    url(r'^view/details$', 'candidate_information',
        name='candidate_information'),
    url(r'^view/microsite$', 'microsite_activity', name='microsite_activity'),
)
