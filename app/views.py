from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.template.response import TemplateResponse, SimpleTemplateResponse
from django.contrib.messages.api import get_messages
from django.contrib.auth.models import User
from social_auth import __version__ as version
from app.forms import CredentialResetForm
from app.helpers import gravatar_link
from app.share import *
import oauth2 as oauth
import logging
logger = logging.getLogger('__name__')


# Semi-static stuff
def about(request):
    """About page. Probably a better way to do this"""
    return render_to_response('about.html', RequestContext(request))

  # TODO Write ajax_login_form
def ajax_login_form(request):
    """Implements login that can be ajaxed into other websites"""
    pass

def ajax_share_form(request):
    """Implements 3rd party share widget"""
    pass

def ajax_user_status(request):
    """Implements login status/settings widget for use on other websites"""   
    ctx = {'avatar':gravatar_link(request.user.email)}
    return render_to_response('user_status.html', ctx, RequestContext(request))

@login_required
def user_view_profile(request):
    """Login complete view, displays user profile on My.Jobs... unless"""

    ctx = {'version': version,
           'last_login': request.session.get('social_auth_last_login_backend'),
           'linked_accounts': request.user.social_auth.all()}
    return render_to_response('done.html', ctx, RequestContext(request))

# TODO: Convert to multilingual-flatpages at some point.
def privacy(request):
    """Privacy page."""
    return render_to_response('privacy.html', RequestContext(request))

def home(request):
    """implements landing page/home page view.
    
    Sends already authenticated users the home page for authenticated users
    """
    if request.user.is_authenticated():
        return HttpResponseRedirect('/profile/')
    else:
        #TODO: Fix home page template.
        return TemplateResponse(request, 'index.html', {})
        #return render_to_response('registration/login.html', {'version': version},
        #                         RequestContext(request))

def profile(request, username):
    """implements user profile view.
    
    Authenticated users go to their own profile get a profile edit view.
    Non-Authenticated users going to a profile get the public profile view.
    Authenticated users goint to someone else's profile get the public profile.
    If no username is passed, 404.
    """

    # throw a 404 if the username does not exist.
    u = get_object_or_404(User, username=username)
    if request.user.is_authenticated():
        # user is logged in
        if request.user == username:
            # is looking at own profile
            render_to_response('myprofile.html', RequestContext(request))
        else:
            # not looking at own profile
            HttpResponseRedirect(u'/public_profile/%s/' % username)
    else:
        # not logged in so show public profile for user
        HttpResponseRedirect(u'/public_profile/%s/' % username)   
    pass

   
def public_profile(request, username):
    """implements public user profile"""
    render_to_response("/public_profile.html", RequestContext(request, {'username':username}))

def coming_soon(request):
    """Placeholder for future features"""
    render_to_response("coming_soon.html")
    
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
    """Universal lost password username connection recovery
    
    Allows for users with multiple accounts using the same email address to
    retreive their credntials.
    """
    
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

@login_required
def edit_profile (request, username):
    """implements edit myjobs profile.
    
    Only allows logged in user to edit their own profile right now. Should be 
    pretty easy to make it so an admin can edit other people's profiles.
    
    parameters:
    
    username -- the username being edited.
    """
    if response.method == "POST":
        pass

def share (request):
    api = access_twitter_api(request.user)
    if request.method == "POST":
        if 'tweet_text' in request.POST:
            tweet = request.POST['tweet_text']
            api.update_status(tweet)
        elif 'message_text' in request.POST:
            username = request.POST['username']
            message = request.POST['message_text']
            api.send_direct_message(screen_name=username, text=message)
        elif 'linkedin_text' in request.POST:
            key, secret = gather_access_token(request.user, 'linkedin')
            token = oauth.Token(key=key, secret=secret)

            consumer = oauth.Consumer(key=LINKEDIN_CONSUMER_KEY,
                                      secret=LINKEDIN_CONSUMER_SECRET)

            uri = 'http://api.linkedin.com/v1/people/~/current-status'
            body = '<?xml version="1.0" encoding="UTF-8"?><current-status>%s</current-status>' % request.POST['linkedin_text'] 
            
            req = oauth.Client(consumer=consumer, token=token)
            
            resp, content = req.request(uri=uri, method='PUT', body=body)
            

            if(content == ''):
                return HttpResponse('success')

        return HttpResponse(content)        
    return render_to_response("tweet.html", RequestContext(request))



