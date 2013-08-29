import operator
import re

from django.conf import settings
from django.utils.text import compress_string
from django.utils.cache import patch_vary_headers

from django import http
from django.core.urlresolvers import reverse

if settings.NEW_RELIC_TRACKING:
    try:
        import newrelic.agent
    except ImportError:
        pass


class RedirectMiddleware:
    """
    Redirects a user to the password change form if several conditions are met:
    - A user is logged in
    - That user's password_change flag is set to True
    - The user is not trying to log out,
        change passwords, or activate an account

    Returns a 403 status code if the request is ajax and the request dict
    contains the 'next' key (i.e. no user is logged in, a privileged
    page was left open, and an unauthorized user tries to access something
    that they shouldn't)
    """
    def process_request(self, request):
        if request.user.is_authenticated():
            urls = [reverse('edit_account'),
                    reverse('edit_password'),
                    reverse('auth_logout'),
                    reverse('registration_activate', args=['a'])[0:-2]]
            url_matches = reduce(operator.or_,
                                 [request.path.startswith(url)
                                  for url in urls])

            if (not url_matches and request.user.password_change):
                return http.HttpResponseRedirect(reverse('edit_account'))

        elif request.is_ajax() and bool(request.REQUEST.get('next')):
            return http.HttpResponse(status=403)


XS_SHARING_ALLOWED_ORIGINS = '*'
XS_SHARING_ALLOWED_METHODS = ['POST','GET','OPTIONS', 'PUT', 'DELETE']
XS_SHARING_ALLOWED_HEADERS = 'Content-Type'


class XsSharing(object):
    """
        This middleware allows cross-domain XHR using the html5 postMessage API.
         

        Access-Control-Allow-Origin: http://foo.example
        Access-Control-Allow-Methods: POST, GET, OPTIONS, PUT, DELETE
    """
    def process_request(self, request):

        if 'HTTP_ACCESS_CONTROL_REQUEST_METHOD' in request.META:
            response = http.HttpResponse()
            response['Access-Control-Allow-Origin']  = XS_SHARING_ALLOWED_ORIGINS 
            response['Access-Control-Allow-Headers']  = XS_SHARING_ALLOWED_HEADERS
            response['Access-Control-Allow-Methods'] = ",".join( XS_SHARING_ALLOWED_METHODS ) 
            
            return response

        return None

    def process_response(self, request, response):
        # Avoid unnecessary work
        if response.has_header('Access-Control-Allow-Origin'):
            return response

        response['Access-Control-Allow-Origin']  = XS_SHARING_ALLOWED_ORIGINS
        response['Access-Control-Allow-Headers']  = XS_SHARING_ALLOWED_HEADERS
        response['Access-Control-Allow-Methods'] = ",".join( XS_SHARING_ALLOWED_METHODS )

        return response 

class NewRelic(object):
    """
    Manages New Relic tracking.

    """
    def process_response(self, request, response):
        if hasattr(request, 'user'):
            newrelic.agent.add_custom_parameter('user_id', request.user.id)
        else:
            newrelic.agent.add_custom_parameter('user_id', 'anonymous')
        return response

    def process_request(self, request):
        if hasattr(request, 'user'):
            newrelic.agent.add_custom_parameter('user_id', request.user.id)
        else:
            newrelic.agent.add_custom_parameter('user_id', 'anonymous')
