import re

from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect


class PasswordChangeMiddleware:
    """
    If a user is logged in, their password_change flag is set, and they
    are not trying to log out, change their password, or activate their
    account, redirect them to the change password form.
    """
    def process_request(self, request):
        if (request.user.is_authenticated() and
            not re.match(reverse('auth_password_change'), request.path) and
            not re.match(reverse('auth_logout'), request.path) and
            not re.match(reverse('registration_activate', args=['a'])[0:-2],
                                 request.path) and
            request.user.password_change):
            return HttpResponseRedirect(reverse('auth_password_change'))
