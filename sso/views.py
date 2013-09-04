import json
from urllib import urlencode
from urllib2 import urlparse, unquote

from django.contrib.auth import authenticate, login, logout
from django.contrib.sessions.models import Session
from django.http import HttpResponse, Http404
from django.template import RequestContext
from django.shortcuts import render_to_response, redirect

from registration.forms import CustomAuthForm
from sso.models import AuthorizedClient


def sso_authorize(request):
    if request.method == 'GET':
        referer = request.META.get('HTTP_REFERER')
        callback = request.GET.get('callback')
        data = {'referer': referer,
                'callback': callback}

        if referer and callback:
            referer = urlparse.urlparse(referer)
            callback = unquote(callback)
            callback = urlparse.urlparse(callback)
            if not (referer.netloc or callback.netloc) or \
                    referer.netloc != callback.netloc:
                raise Http404
        else:
            # Do we want to show 404 pages everywhere?
            raise Http404

        data['referer_short'] = referer.netloc

        if not request.user.is_anonymous():
            good_key = request.session.get('key')
            test_key = request.GET.get('key')
            if good_key:
                if test_key:
                    if test_key == good_key:
                        if request.user.authorizedclient_set.filter(
                                site=referer.netloc):
                            request.session.set_expiry(None)

                            q = urlparse.parse_qs(callback.query)
                            q.update({'key': good_key})
                            callback = callback._replace(query=urlencode(q))
                            return redirect(urlparse.urlunparse(callback))
                        else:
                            return render_to_response('sso/sso_auth.html',
                                                      data,
                                                      RequestContext(request))
                    else:
                        logout(request)
                else:
                    return render_to_response('sso/sso_auth.html',
                                              data,
                                              RequestContext(request))
            else:
                request.session['key'] = AuthorizedClient.create_key(
                    request.user)
                if test_key:
                    logout(request)
                else:
                    return render_to_response('sso/sso_auth.html',
                                              data,
                                              RequestContext(request))

        login_form = CustomAuthForm(auto_id=True)
        data['login_form'] = login_form
        return render_to_response('sso/sso_auth.html',
                                  data,
                                  RequestContext(request))

    else:
        action = request.POST.get('action')
        referer = request.POST.get('referer')
        callback = request.POST.get('callback')
        data = {'referer': referer,
                'callback': callback}
        referer = urlparse.urlparse(referer)
        if action == 'login':
            login_form = CustomAuthForm(data=request.POST, auto_id=False)
            if login_form.is_valid():
                user = authenticate(
                    username=login_form.cleaned_data['username'],
                    password=login_form.cleaned_data['password'])
                login(request, user)
                request.session.set_expiry(None)
            else:
                data['login_form'] = login_form
                data['referer_short'] = referer.netloc
                return render_to_response('sso/sso_auth.html', data,
                                          RequestContext(request))

        request.user.authorizedclient_set.get_or_create(site=referer.netloc)

        if not request.session.get('key'):
            request.session['key'] = AuthorizedClient.create_key(request.user)

        callback = request.POST.get('callback')
        callback = urlparse.urlparse(callback)
        q = urlparse.parse_qs(callback.query)
        q.update({'key': request.session['key']})
        callback = callback._replace(query=urlencode(q))
        return redirect(urlparse.urlunparse(callback))
