from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
# imports for using the login form obect on the homepage. Probably not
# needed, but preserved until we are sure. JPS 10-12-12
from django.contrib.auth import REDIRECT_FIELD_NAME, login as auth_login
from django.contrib.auth.forms import AuthenticationForm
# end login form imports section
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.template.response import TemplateResponse, SimpleTemplateResponse
from django.contrib import messages
from django.contrib.auth.models import User
from social_auth import __version__ as version
from app.forms import CredentialResetForm
from app.helpers import gravatar_link
from app.share import *
from tweepy.error import *
from facebook import GraphAPIError
import logging
logger = logging.getLogger('__name__')
from registration import views as RegistrationViews
from registration.backends.default import DefaultBackend

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
    request.session['origin'] = 'main'
    linked_accounts = request.user.social_auth.all()
    account_info = []
    for account in linked_accounts:
        account_info.append({'name': account.provider,
                             'image': STATIC_URL+'social-icons/'+
                             account.provider.capitalize()+'.png'})
    ctx = {'version': version,
           'last_login': request.session.get('social_auth_last_login_backend'),
           'account_info': account_info}
    return render_to_response('done.html', ctx, RequestContext(request))

# TODO: Convert to multilingual-flatpages at some point.
def privacy(request):
    """Privacy page."""
    return render_to_response('privacy.html', RequestContext(request))

def home(request,redirect_field_name=REDIRECT_FIELD_NAME,
         authentication_form=AuthenticationForm):
    """    
    Handles the homepage display.
    
    I have left the functionality for sending the login form object via this
    view in the comments, because I am not certain we don't need it.
    [JPS 10-12-12]
    
    Inputs:
    :request:               django request object
    :redirect_field_name:   form field name that contains the next page
    :authentication_form:   django.contrib.auth authentication form method
    
    """
    request.session['origin'] = 'main'
    redirect_to = request.REQUEST.get(redirect_field_name, '')
    form=authentication_form(request)
    
    #context = {
    #    'form': form,
    #    redirect_field_name: redirect_to,
    #}
    context = {}
    return TemplateResponse(request, 'index.html', context)
        

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
    request.session['origin'] = 'main'
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

@login_required
def share (request, provider):
    data_dict={'provider':provider,
               'url': request.session.get('share_url')}

    if request.method == "POST":
        message = request.POST['status_text']
        link = request.session.get('share_url')
        if provider == 'linkedin':
            try:
                linkedin_api = access_linkedin_api(request.user)
                uri = 'http://api.linkedin.com/v1/people/~/shares'
                body = build_linkedin_share(message,submitted_url=link)
                resp, content = linkedin_api.request(uri=uri, method='POST',
                                                     body=body,
                                                     headers={'Content-Type': 'text/xml'})
                messages.success(request, "Status successfully posted!")
            except:
                messages.error(request, ("%s" % content))
        elif provider == 'facebook':
            try:
                facebook_api = access_facebook_api(request.user)
                facebook_api.put_object("me","links",
                                        picture='http://src.nlx.org/myjobs/icon-80x80.png',
                                        message=message,
                                        link=link,
                                        name='My Jobs',
                                        caption='Real jobs from real companies')
                message.success(request, "Status successfully posted!")
            except GraphAPIError, e:
                messages.error(request, ("%s" % e.reason))                
        elif provider == 'twitter':
            twitter_api = access_twitter_api(request.user)
            try:
                twitter_api.update_status(message)
                messages.success(request, "Status successfully posted!")
            except TweepError, e:
                messages.error(request, ("%s" % e.reason))                
    return render_to_response("share.html", data_dict,
                              context_instance=RequestContext(request))

def auth_popup(request, provider):
    """
    Handles share pop up redirects. If user needs to get authenticated,
    it redirects to the authentication page. Otherwise, it goes straight to
    the share form. This also stores session information used in login_redirect
    and to maintain the data needed for sharing.

    Input:
    :provider: String name of the third party provider to be shared to.
    
    """
    request.session['origin'] = 'share'
    request.session['share_provider'] = provider
    request.session['share_url'] = request.GET.get('url')
    if request.user.is_authenticated():
        if request.user.social_auth.filter(provider=provider):
            return HttpResponseRedirect('/share/%s' % provider)
        else:
            return HttpResponseRedirect('/login/'+provider)
    else:
        return HttpResponseRedirect('/login/'+provider)

def login_redirect(request):
    """
    Handles the redirects coming from the authentication process.
    By default, this always redirects to the profile page so we use the session
    information to redirect to the share form when necessary.
    
    """
    if request.session.get('origin')=='share':
        provider = request.session.get('share_provider')
        return HttpResponseRedirect('/share/%s' % provider)
    else:
        return HttpResponseRedirect('/profile')

def remove_association(request,provider):
    request.session['origin'] = 'main'
    provider=request.user.social_auth.get(provider=provider)
    provider.delete()
    return HttpResponseRedirect('/profile')
