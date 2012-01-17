from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.messages.api import get_messages
from django.contrib.auth.models import User
from social_auth import __version__ as version
from app.forms import CredentialResetForm

import logging
logger = logging.getLogger('__name__')


# Semi-static stuff
def about(request):
    """About page. Probably a better way to do this"""
    return render_to_response('about.html', RequestContext(request))

def privacy(request):
    """Privacy page."""
    return render_to_response('privacy.html', RequestContext(request))

def home(request):
    """implements landing page/home page view.
    
    Sends already authenticated users the home page for authenticated users
    """
    if request.user.is_authenticated():
        return HttpResponseRedirect('/profile')
    else:
        return HttpResponseRedirect('/')
    #return render_to_response('login.html', {'version': version},
    #                              RequestContext(request))

@login_required
def profile(request, username):
    """implements user profile view.
    
    Authenticated users going to their own profile get a profile edit view.
    Non-Authenticated users going to a profile get the public profile view.
    Authenticated users goint to someone else's profile get the public profile.
    If no username is passed, 404.
    """
    url = request.user.get_profile().url
    pass

@login_required
def done(request):
    """Login complete view, displays user data"""
    ctx = {'version': version,
           'last_login': request.session.get('social_auth_last_login_backend')}
    return render_to_response('done.html', ctx, RequestContext(request))

def error(request):
    """Error view"""
    messages = get_messages(request)
    return render_to_response('error.html', {'version': version,
                              'messages': messages}, RequestContext(request))

def logout(request):
    """Logs out user"""
    auth_logout(request)
    return HttpResponseRedirect('/')


def password_connection(request, is_admin_site=False,
	                   template_name='registration/password_reset_form.html',
	                   email_template_name='registration/multi_reset_email.html',
	                   password_reset_form=CredentialResetForm,
	                   token_generator=default_token_generator,
	                   post_reset_redirect=None,
	                   from_email=None,
	                   current_app=None,
	                   extra_context=None):
    """Universal lost password username connection recovery"""
    
    if post_reset_redirect is None:
        post_reset_redirect = reverse('auth_password_reset_done')
    if request.method == "POST":
        form = CredentialResetForm(request.POST)
        
        if form.is_valid():
            opts = {
                'use_https': request.is_secure(),
                'token_generator': token_generator,
                'from_email': from_email,
                'email_template_name': email_template_name,
                'request': request,
            }
            if is_admin_site:
                opts = dict(opts, domain_override=request.META['HTTP_HOST'])
            form.save(**opts)
            return HttpResponseRedirect(post_reset_redirect)
    else:
        form = password_reset_form()
    context = { 'form': form,}
    context.update(extra_context or {})
    return render_to_response(template_name, context,
                context_instance=RequestContext(request, current_app=current_app))
