import json
from urllib import urlencode
from urllib2 import unquote, urlparse

from django.contrib.auth import authenticate, login, logout
from django.contrib.sessions.models import Session
from django.http import HttpResponse, Http404
from django.template import RequestContext
from django.shortcuts import render_to_response, redirect

from registration.forms import CustomAuthForm
from sso.models import AuthorizedClient


def sso_authorize(request):
    """
    Authorizes specific web sites to utilize an existing My.jobs account
    """
    if request.method == 'GET':
        # Initial view after being redirected from an external site
        referer = request.META.get('HTTP_REFERER')
        callback = request.GET.get('callback')
        data = {'referer': referer,
                'callback': callback}

        if referer and callback:
            # referer and callback are required
            referer = urlparse.urlparse(referer)
            callback = unquote(callback)
            callback = urlparse.urlparse(callback)
            if not (referer.netloc and callback.netloc) or \
                    referer.netloc != callback.netloc:
                # If the base urls of referer and callback are not truthy,
                # the urls are malformed somehow.
                # These are expected to be truthy and equal to one another.
                raise Http404
        else:
            raise Http404

        data['referer_short'] = referer.netloc

        if not request.user.is_anonymous():
            # Process logged in users first; Certain criteria may cause the
            # user to be logged out.
            good_key = request.session.get('key')
            test_key = request.GET.get('key')
            if good_key:
                # The current user already has a key available.
                if test_key:
                    # The remote site has provided a key; the user has
                    # potentially already authorized this site.
                    if test_key == good_key:
                        if request.user.authorizedclient_set.filter(
                                site=referer.netloc):
                            # The user has authorized this site; Reset the
                            # current session expiry, add the key to the
                            # callback url, and redirect to it.
                            request.session.set_expiry(None)

                            q = urlparse.parse_qs(callback.query)
                            q.update({'key': good_key})
                            callback = callback._replace(
                                query=urlencode(q))
                            return redirect(urlparse.urlunparse(callback))
                        else:
                            # The user at one time authorized this site but it
                            # was revoked (potential future functionality?).
                            # Ask for authorization again.
                            return render_to_response('sso/sso_auth.html',
                                                      data,
                                                      RequestContext(request))
                    else:
                        # The key provided does not match the user's key; Log
                        # the user out. It may be a different user's key.
                        logout(request)
                else:
                    # No key was provided; Proceed to authorization normally.
                    return render_to_response('sso/sso_auth.html',
                                              data,
                                              RequestContext(request))
            else:
                # The user has no key; Create one.
                request.session['key'] = AuthorizedClient.create_key(
                    request.user)
                if test_key:
                    # A key was provided, but the current user did not have one
                    # until now. Log out the user.
                    logout(request)
                else:
                    # No key was provided; Proceed to authorization.
                    return render_to_response('sso/sso_auth.html',
                                              data,
                                              RequestContext(request))

        # Only anonymous users can reach this point. This is not inside an else
        # block so that it can catch users who were logged out above.
        login_form = CustomAuthForm(auto_id=True)
        data['login_form'] = login_form
        return render_to_response('sso/sso_auth.html',
                                  data,
                                  RequestContext(request))

    else:
        # Form was posted.
        action = request.POST.get('action')
        referer = request.POST.get('referer')
        callback = request.POST.get('callback')
        data = {'referer': referer,
                'callback': callback}
        referer = urlparse.urlparse(referer)
        callback = urlparse.urlparse(callback)
        if action == 'login':
            login_form = CustomAuthForm(data=request.POST, auto_id=False)
            if login_form.is_valid():
                user = authenticate(
                    username=login_form.cleaned_data['username'],
                    password=login_form.cleaned_data['password'])
                login(request, user)
                request.session.set_expiry(None)
                # User was logged in. Fall through to code common to
                # preauthenticated users
            else:
                data['login_form'] = login_form
                data['referer_short'] = referer.netloc
                return render_to_response('sso/sso_auth.html', data,
                                          RequestContext(request))

        # Ensure that an AuthorizedClient instance exists for the current user
        # and the site that is requesting authorization.
        request.user.authorizedclient_set.get_or_create(site=referer.netloc)

        # Ensure that the current user has a key.
        if not request.session.get('key'):
            request.session['key'] = AuthorizedClient.create_key(request.user)

        # Add the user's key to the callback url and redirect to it.
        q = urlparse.parse_qs(callback.query)
        q.update({'key': request.session.get('key')})
        callback = callback._replace(query=urlencode(q))
        return redirect(urlparse.urlunparse(callback))
