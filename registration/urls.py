from django.conf.urls.defaults import *
from django.contrib.auth import views as auth_views

from registration.forms import CustomAuthForm, CustomPasswordResetForm
from registration.views import *

# Authorization URLS
urlpatterns = patterns('',
                       url(r'^logout/$',
                           auth_views.logout,
                           {'next_page': '/'},
                           name='auth_logout'),
                       url(r'^password/reset/$',
                           auth_views.password_reset,
                           {'password_reset_form': CustomPasswordResetForm},
                           name='auth_password_reset'),
                       url(r'^password/reset/confirm/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$',
                           auth_views.password_reset_confirm,
                           name='auth_password_reset_confirm'),
                       url(r'^password/reset/complete/$',
                           auth_views.password_reset_complete,
                           name='auth_password_reset_complete'),
                       url(r'^password/reset/done/$',
                           auth_views.password_reset_done,
                           name='auth_password_reset_done'),
)

#Registration URLS
urlpatterns += patterns('',
                        url(r'^register/$', register, name='register'),
                        url(r'^activate/(?P<activation_key>\w+)/$', activate,
                            name='registration_activate'),
                        url(r'^register/resend/$', resend_activation,
                            name='resend_activation'),
                        url(r'^register/complete/$', RegistrationComplete.as_view(),
                            name='register_complete'),
)
