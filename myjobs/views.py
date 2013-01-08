import logging

from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.views.generic import TemplateView

from myjobs.forms import *
from registration.forms import *



logger = logging.getLogger('__name__')


class About(TemplateView):
    template_name = "about.html"


class Privacy(TemplateView):
    template_name = "privacy.html"


def home(request):
    """
    The home page takes AJAX requests from the front end for account creation.
    If an account is successfully created, this view returns a simple 'valid'
    HTTP Response, which the front end jQuery recognizes as a signal to continue
    with the account creation process. If an error occurs in the form, this view
    returns an updated registration form showing the errors.

    """
    registrationform =  RegistrationForm(auto_id=False)
    loginform = CustomAuthForm(auto_id=False)
    if request.method == "POST":
        if request.POST['action'] == "register":
            registrationform = RegistrationForm(request.POST, auto_id=False)
            if registrationform.is_valid():
                new_user = User.objects.create_inactive_user(**registrationform.cleaned_data)
                user_cache = authenticate(username = registrationform.cleaned_data['email'],
                                          password = registrationform.cleaned_data['password1'])
                login(request, user_cache)
                return HttpResponse('valid')
            else:
                return render_to_response('includes/widget-user-registration.html',
                                          {'form': registrationform},
                                          context_instance=RequestContext(request))
                                          
        elif request.POST['action'] == "login":
            loginform = CustomAuthForm(request.POST)
            if loginform.is_valid():
                login(request, loginform.get_user())
                return HttpResponseRedirect('/account')
    ctx = {'registrationform':registrationform,
           'loginform': loginform}
    return render_to_response('index.html', ctx, RequestContext(request))

    
@login_required
def view_account(request):
    """Login complete view, displays user profile on My.Jobs... unless"""
    return render_to_response('done.html', RequestContext(request))

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
            form.save()
            return HttpResponseRedirect('/account')
    else:
        form = ChangePasswordForm(user=request.user)
    ctx = {'form':form}
    return render_to_response('registration/password_change_form.html', ctx,
                              RequestContext(request))

def error(request):
    """Error view"""
    messages = get_messages(request)
    return render_to_response('error.html', {'version': version,
                              'messages': messages}, RequestContext(request))
        
