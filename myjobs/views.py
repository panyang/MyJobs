import base64
import datetime
import json
import logging
import urllib2

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import user_passes_test, login_required
from django.core.urlresolvers import reverse
from django.forms.models import model_to_dict
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.utils.html import mark_safe
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView

from myjobs.models import User, EmailLog
from myjobs.forms import *
from myjobs.helpers import *
from myprofile.forms import *
from registration.forms import *

logger = logging.getLogger('__name__')

class About(TemplateView):
    template_name = "about.html"


class Privacy(TemplateView):
    template_name = "privacy-policy.html"


class Terms(TemplateView):
    template_name = "terms.html"


def home(request):
    """
    The home page view receives 2 separate Ajax requests, one for the registration
    form and another for the initial profile information form. If everything
    checks out alright and the form saves with no errors, it returns a simple string,
    'valid', as an HTTP Response, which the front end recognizes as a signal to
    continue with the account creation process. If an error occurs, this triggers
    the jQuery to update the page. The form instances with errors must be passed
    back to the form template it was originally from.

    """

    # TODO - rename using snake case
    registrationform = RegistrationForm(auto_id=False)
    loginform = CustomAuthForm(auto_id=False)

    name_form = InitialNameForm(prefix="name")
    education_form = InitialEducationForm(prefix="edu")
    phone_form = InitialPhoneForm(prefix="ph")
    work_form = InitialWorkForm(prefix="work")
    address_form = InitialAddressForm(prefix="addr")
        
    data_dict = {'registrationform':registrationform,
                 'loginform': loginform,
                 'name_form': name_form,
                 'phone_form': phone_form,
                 'address_form': address_form,
                 'work_form': work_form,
                 'education_form': education_form,
                 'name_obj': get_name_obj(request)}

    if request.method == "POST":
        if request.POST['action'] == "register":
            registrationform = RegistrationForm(request.POST, auto_id=False)
            if registrationform.is_valid():
                new_user, created = User.objects.create_inactive_user(**registrationform.
                                                             cleaned_data)
                user_cache = authenticate(username = registrationform.
                                          cleaned_data['email'],
                                          password = registrationform.
                                          cleaned_data['password1'])
                login(request, user_cache)
                # pass in gravatar url once user is logged in. Image generated
                # on AJAX success
                data={'gravatar_url': new_user.get_gravatar_url(size=100)}
                return HttpResponse(json.dumps(data))
            else:
                return render_to_response('includes/widget-user-registration.html',
                                          {'form': registrationform},
                                          context_instance=RequestContext(request))

        elif request.POST['action'] == "login":
            loginform = CustomAuthForm(data=request.POST)
            if loginform.is_valid():
                login(request, loginform.get_user())
                return HttpResponse('valid')
            else:
                return render_to_response('includes/widget-login-username.html',
                                          {'form': loginform},
                                          context_instance=RequestContext(request))
        elif request.POST['action'] == "save_profile":
            name_form = InitialNameForm(request.POST, prefix="name", user=request.user)
            education_form = InitialEducationForm(request.POST, prefix="edu", user=request.user)
            phone_form = InitialPhoneForm(request.POST, prefix="ph", user=request.user)
            work_form = InitialWorkForm(request.POST, prefix="work", user=request.user)
            address_form = InitialAddressForm(request.POST, prefix="addr", user=request.user)

            forms = [name_form, education_form, phone_form, work_form, 
                    address_form]
            valid_forms = [form for form in forms if form.is_valid()]
            invalid_forms = []
            for form in forms:
                if form.changed_data and not form.is_valid():
                    invalid_forms.append(form)

            if not invalid_forms:
                for form in valid_forms:
                    form.save(commit=False)
                    form.user = request.user
                    form.save_m2m()
                return HttpResponse('valid')
            else:
                return render_to_response('includes/initial-profile-form.html',
                                          {'name_form': name_form,
                                           'phone_form': phone_form,
                                           'address_form': address_form,
                                           'work_form': work_form,
                                           'education_form': education_form},
                                          context_instance=RequestContext(request))
            
    return render_to_response('index.html', data_dict, RequestContext(request))

    
@login_required
def view_account(request):
    ctx = {'name_obj': get_name_obj(request)}
    return render_to_response('done.html', ctx, RequestContext(request))

@user_passes_test(User.objects.not_disabled)
def edit_account(request):
    initial_dict = model_to_dict(request.user)
    name_obj = get_name_obj(request)
    if name_obj:
        initial_dict.update(model_to_dict(name_obj))

    ctx = {'user': request.user,
           'gravatar_100': request.user.get_gravatar_url(size=100),
           'name_obj': name_obj}

    if request.user.password_change:
        resp = edit_password(request)
        ctx['change_pass'] = mark_safe(resp.content)
    else:
        form = EditAccountForm(initial=initial_dict, user=request.user)
        if request.method == "POST":
            form = EditAccountForm(user=request.user, data=request.POST)
            if form.is_valid():
                form.save(request.user)
                return HttpResponse('success')
        ctx['form'] = form
           
    
    return render_to_response('myjobs/edit-account.html', ctx,
                              RequestContext(request))

@user_passes_test(User.objects.not_disabled)
def edit_basic(request):
    initial_dict = model_to_dict(request.user)
    name_obj = get_name_obj(request)
    if name_obj:
        initial_dict.update(model_to_dict(name_obj))

    form = EditAccountForm(initial=initial_dict, user=request.user)        
    if request.method == "POST":
        form = EditAccountForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save(request.user)
            return HttpResponse('success')

    ctx = {'form': form,
           'gravatar_100': request.user.get_gravatar_url(size=100),
           'section_name': 'basic'}
           
    return render_to_response('myjobs/edit-form-template.html', ctx,
                              RequestContext(request))
    

@user_passes_test(User.objects.not_disabled)
def edit_communication(request):
    obj = User.objects.get(id=request.user.id)

    form = EditCommunicationForm(user=request.user, instance=obj)
    if request.method == "POST":
        form = EditCommunicationForm(user=request.user, instance=obj,
                                     data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse('success')
    
    ctx = {'form': form,
           'section_name': 'communication'}
    
    return render_to_response('myjobs/edit-form-template.html', ctx,
                              RequestContext(request))

    
    
@user_passes_test(User.objects.not_disabled)
def edit_password(request):
    form = ChangePasswordForm()
    if request.method == "POST":
        form = ChangePasswordForm(user=request.user, data=request.POST)
        if form.is_valid():
            request.user.password_change = False
            request.user.save()
            form.save()
            return HttpResponse('success')

    ctx = {'form':form,
           'section_name': 'password'}
    return render_to_response('myjobs/edit-form-template.html', ctx,
                              RequestContext(request))

@user_passes_test(User.objects.not_disabled)
def edit_delete(request):
    ctx = {'gravatar_150': request.user.get_gravatar_url(size=150),
           'name_obj': get_name_obj(request)}
    return render_to_response('myjobs/edit-delete.html', ctx,
                              RequestContext(request))

@user_passes_test(User.objects.not_disabled)
def edit_disable(request):
    ctx = {'gravatar_150': request.user.get_gravatar_url(size=150),
           'name_obj': get_name_obj(request)}
    return render_to_response('myjobs/edit-disable.html', ctx,
                              RequestContext(request))

        
@user_passes_test(User.objects.not_disabled)
def delete_account(request):
    email = request.user.email
    request.user.delete()
    ctx = {'name_obj': get_name_obj(request),'email': email}
    return render_to_response('myjobs/delete-account-confirmation.html', ctx,
                              RequestContext(request))

@user_passes_test(User.objects.not_disabled)
def disable_account(request):
    user = request.user
    email = user.email
    user.disable()
    logout(request)
    ctx = {'email': email,'name_obj': get_name_obj(request)}
    return render_to_response('myjobs/disable-account-confirmation.html', ctx,
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

@csrf_exempt
def batch_message_digest(request):
    """
    Used by SendGrid to POST batch events.

    Accepts a POST request containing a batch of events from SendGrid. A batch
    of events is a series of JSON strings separated by new lines.
    """
    if 'HTTP_AUTHORIZATION' in request.META:
        method, details = request.META['HTTP_AUTHORIZATION'].split()
        if method.lower() == 'basic':
            # login_info is intended to be a base64-encoded string in the format
            # "email:password" where email is a urlquoted string
            login_info = base64.b64decode(details).split(':')
            if len(login_info) == 2:
                login_info[0] = urllib2.unquote(login_info[0])
                user = authenticate(email=login_info[0], password=login_info[1])
                target_user = User.objects.get(email='accounts@my.jobs')
                if user is not None and user == target_user:
                    events = request.raw_post_data
                    event_list = []
                    try:
                        # Handles both a lack of submitted data and
                        # the submission of invalid data
                        events = events.splitlines()
                        for event_str in events:
                            if event_str == '':
                                continue
                            event_list.append(json.loads(event_str))
                    except:
                        return HttpResponse(status=400)
                    for event in event_list:
                        EmailLog(email=event['email'], event=event['event'],
                                 received=datetime.date.fromtimestamp(
                                     float(event['timestamp'])
                                 )
                        ).save()
                    return HttpResponse(status=200)
    return HttpResponse(status=403)

@user_passes_test(User.objects.not_disabled)
def continue_sending_mail(request):
    """
    Updates the user's last response time to right now.
    Allows the user to choose to continue receiving emails if they are inactive.
    """
    user = request.user
    user.last_response = datetime.date.today()
    user.save()
    return redirect('/')
