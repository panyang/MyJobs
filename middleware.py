import re

from django.utils.text import compress_string
from django.utils.cache import patch_vary_headers

from django import http
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
            not re.match(reverse('edit_password'), request.path) and
            not re.match(reverse('auth_logout'), request.path) and
            not re.match(reverse('registration_activate', args=['a'])[0:-2],
                                 request.path) and
            request.user.password_change):
            return HttpResponseRedirect(reverse('edit_password'))



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
