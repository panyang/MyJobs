import re

from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

class PasswordChangeMiddleware:
    def process_request(self, request):
        if request.user.is_authenticated() and \
            not re.match(reverse('auth_password_change'), request.path) and \
            not re.match(reverse('auth_logout'), request.path) and \
            not re.match('/accounts/activate/', request.path) and \
            request.user.password_change:
                return HttpResponseRedirect(reverse('auth_password_change'))
