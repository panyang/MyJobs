from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.template.response import TemplateResponse, SimpleTemplateResponse
from django.contrib import messages
from django.views.generic import TemplateView
from social_auth import __version__ as version

from app.forms import *
from app.share import *
from tweepy.error import *
from facebook import GraphAPIError
from registration.forms import *
import logging

logger = logging.getLogger('__name__')

class About(TemplateView):
    template_name = "about.html"

class Privacy(TemplateView):
    template_name = "privacy.html"

@login_required
def view_account(request):
    """Login complete view, displays user profile on My.Jobs... unless"""
    request.session['origin'] = 'main'
    #linked_accounts = request.user.social_auth.all()
    account_info = []
    # for account in linked_accounts:
    #     account_info.append({'name': account.provider,
    #                          'image': STATIC_URL+'social-icons/'+
    #                          account.provider.capitalize()+'.png'})
    ctx = {'version': version,
           'last_login': request.session.get('social_auth_last_login_backend'),
           'account_info': account_info}    
    return render_to_response('done.html', ctx, RequestContext(request))


def home(request):
    request.session['origin'] = 'main'
    if request.method == "POST":
        if 'register' in request.POST:
            registrationform = RegistrationForm(request.POST)
            if registrationform.is_valid():
                new_user = User.objects.create_inactive_user(**form.cleaned_data)
                return HttpResponseRedirect('/accounts/register/complete')
        elif 'login' in request.POST:
            loginform = CustomAuthForm(request.POST)
            if loginform.is_valid():
                login(request, loginform.get_user())
                return HttpResponseRedirect('/account')
    else:
        registrationform =  RegistrationForm()
        loginform = CustomAuthForm()

    ctx = {'registrationform':registrationform,
           'loginform': loginform}
    return render_to_response('index.html', ctx, RequestContext(request))

def error(request):
    """Error view"""
    messages = get_messages(request)
    return render_to_response('error.html', {'version': version,
                              'messages': messages}, RequestContext(request))
        
@login_required
def edit_account(request):
    user_instance = User.objects.filter(id=request.user.id).values()[0]
    if request.method == "POST":
        form = EditProfileForm(request.POST)
        if form.is_valid():
            form.save(request.user)
            return HttpResponseRedirect('/account')
    else:
        form = EditProfileForm(user_instance)

    ctx = {'form': form,
           'user': request.user}
    return render_to_response('edit-account.html', ctx,
                              RequestContext(request))

@login_required
def change_password(request):
    if request.method == "POST":
        form = ChangePasswordForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save(request.user)
            return HttpResponseRedirect('/account')
    else:
        form = ChangePasswordForm()
    ctx = {'form':form}
    return render_to_response('registration/password_change_form.html', ctx,
                              RequestContext(request))
            
    
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
#    provider=request.user.social_auth.get(provider=provider)
    provider.delete()
    return HttpResponseRedirect('/profile')
