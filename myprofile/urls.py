from django.conf.urls import patterns, url


urlpatterns = patterns('MyJobs.myprofile.views',
    url(r'^$', 'edit_profile', name='view_profile'),
    url(r'^delete/(?P<item_id>\d+)/$', 'delete_item', name='delete_item'),
    url(r'^edit/$', 'handle_form', name='handle_form'),
    url(r'^details/$', 'get_details', name='get_details'),
)
