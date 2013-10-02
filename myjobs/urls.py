from django.conf.urls import patterns, url, include
from django.views.generic import RedirectView

from myjobs.views import *

editpatterns = patterns('MyJobs.myjobs.views',
    url(r'^basic$', 'edit_basic', name='edit_basic'),
    url(r'^password$', 'edit_password', name='edit_password'),
    url(r'^delete$', 'edit_delete', name='edit_delete'),
    url(r'^disable$', 'edit_disable', name='edit_disable'),
    url(r'^communication$', 'edit_communication', name='edit_communication'),
)

accountpatterns = patterns('MyJobs.myjobs.views',
    url(r'^edit/$', 'edit_account', name='edit_account'),
    url(r'^delete$', 'delete_account', name='delete_account'),
    url(r'^disable$', 'disable_account', name='disable_account'),
    url(r'^$',
        RedirectView.as_view(url='/account/edit/')),
)

urlpatterns = patterns('MyJobs.myjobs.views',
    url(r'^$', 'home', name='home'),
    url(r'^about/$', About.as_view(), name='about'),
    url(r'^privacy/$', Privacy.as_view(), name='privacy'),
    url(r'^terms/$', Terms.as_view(), name='terms'),
    url(r'^contact/$', 'contact', name='contact'),
    url(r'^batch$', 'batch_message_digest', name='batch_message_digest'),
    url(r'^unsubscribe/$', unsubscribe_all, name='unsubscribe_all'),
    url(r'^account/', include(accountpatterns)),
    url(r'^account/edit/', include(editpatterns)),
    url(r'^send/$', 'continue_sending_mail', name='continue_sending_mail'),
    url(r'^toolbar/$', 'toolbar', name='toolbar'),
)
