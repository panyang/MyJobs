from django import http
from django.core import request
from django.conf import settings

from shorty.models import Shorty

class ShortyFallbackMiddleware(object):
    """Checks for short URL and redirects on 404s"""
    def process_response(self, request, response):
        if response.status_code != 404:
            return response
        path = request.get_full_path()
        # Get shorty and redirect
        try:
            s = Shorty.objects.get(from_site__iexact=settings.SITE_ID,
                                   shorty__iexact=)
        except Redirect.DoesNotExist:
            r = None
        if r is None and settings.APPEND_SLASH:
            # Try removing the trailing slash.
            try:
                r = Redirect.objects.get(site__id__exact=settings.SITE_ID,
                    old_path=path[:path.rfind('/')]+path[path.rfind('/')+1:])
            # Fail gracefully so another middleware can grab response
            except Redirect.DoesNotExist:
                pass
        if r is not None:
            if r.new_path == '':
                return http.HttpResponseGone()

        if 
            return http.HttpResponsePermanentRedirect(r.new_path)

        # No redirect was found. Return the response.
        return response
