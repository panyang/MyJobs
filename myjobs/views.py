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
from myprofile.forms import *
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
    returns an updated registratiocn form showing the errors.

    """
    registrationform = RegistrationForm(auto_id=False)
    loginform = CustomAuthForm(auto_id=False)

    nameform = NameForm(auto_id=False)
    emailform = SecondaryEmailForm(auto_id=False)
        
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
        elif request.POST['action'] == "save_profile":
            nameform = NameForm(request.POST, user=request.user, auto_id=False)
            emailform = SecondaryEmailForm(request.POST, user=request.user,
                                           auto_id=False)
            
            if nameform.is_valid() and emailform.is_valid():
                nameform.save()
                emailform.save()
                return HttpResponse('Valid')
            else:
                return render_to_response('includes/widget-user-registration.html',
                                          {'form': registrationform},
                                          context_instance=RequestContext(request))
    ctx = {'registrationform':registrationform,
           'loginform': loginform,
           'given_name': given_name,
           'nameform': nameform,
           'emailform': emailform,            
           'name_obj': get_name_obj(request)}
    return render_to_response('index.html', ctx, RequestContext(request))

    
@login_required
def view_account(request):
    """Login complete view, displays user profile on My.Jobs"""
    ctx = {'name_obj': get_name_obj(request)}
    return render_to_response('done.html', ctx, RequestContext(request))

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
           'user': request.user,
           'name_obj': get_name_obj(request)
            }
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
    
    ctx = {
        'form':form,
        'name_obj': get_name_obj(request)
        }
    return render_to_response('registration/password_change_form.html', ctx,
                              RequestContext(request))

def error(request):
    """Error view"""
    messages = get_messages(request)
    ctx = {
        'name_obj': get_name_object(request),
        'version': version,
        'messages': messages
        }
    return render_to_response('error.html', ctx, RequestContext(request))

def get_name_obj(request):
    """
    A utility function that returns the user name object for inclusion in the
    view context.
    
    Inputs:
    :request:   request object
    
    Returns:
    :name_obj:  User's display name (str)|None
    
    """
    try:
        name_obj = Name.objects.get(user=request.user,primary=True)
    except (Name.DoesNotExist,TypeError):
        name_obj = None
    return name_obj
