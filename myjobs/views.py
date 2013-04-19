import datetime
import json
import logging

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import user_passes_test, login_required
from django.core.urlresolvers import reverse
from django.forms.models import model_to_dict
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404, redirect
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
    template_name = "privacy.html"


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


    registrationform = RegistrationForm(auto_id=False)
    loginform = CustomAuthForm(auto_id=False)

    
    # Parameters passed into the form class. See forms.py in myprofile
    # for more detailed docs
    settings = {'auto_id':False, 'empty_permitted':True, 'only_show_required':True,
                'user': request.user}
    settings_show_all = {'auto_id':False, 'empty_permitted':True,
                         'only_show_required':False, 'user': request.user}
    
    name_form = instantiate_profile_forms(request,[NameForm],settings)[0]
    education_form = instantiate_profile_forms(request,[EducationForm],
                                               settings)[0]
    phone_form = instantiate_profile_forms(request,[TelephoneForm],settings)[0]
    work_form = instantiate_profile_forms(request,[EmploymentHistoryForm],settings)[0]
    address_form = instantiate_profile_forms(request,[AddressForm],settings)[0]

        
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
                new_user = User.objects.create_inactive_user(**registrationform.
                                                             cleaned_data)
                user_cache = authenticate(username = registrationform.
                                          cleaned_data['email'],
                                          password = registrationform.
                                          cleaned_data['password1'])
                login(request, user_cache)
                # pass in gravatar url once user is logged in. Image generated
                # in AJAX success
                data={'gravatar_url': new_user.get_gravatar_url(size=100)}
                return HttpResponse(json.dumps(data))
            else:
                return render_to_response('includes/widget-user-registration.html',
                                          {'form': registrationform},
                                          context_instance=RequestContext(request))

        elif request.POST['action'] == "login":
            loginform = CustomAuthForm(request.POST)
            if loginform.is_valid():
                login(request, loginform.get_user())
                return HttpResponseRedirect('/profile')
                
        elif request.POST['action'] == "save_profile":
            # rebuild the form object with the post parameter = True            
            name_form = instantiate_profile_forms(request,[NameForm],
                                                  settings,post=True)[0]
            education_form = instantiate_profile_forms(request,[EducationForm],
                                                  settings,post=True)[0]
            phone_form = instantiate_profile_forms(request,[TelephoneForm],
                                                  settings,post=True)[0]
            work_form = instantiate_profile_forms(request,[EmploymentHistoryForm],
                                                  settings,post=True)[0]
            address_form = instantiate_profile_forms(request,[AddressForm],
                                                  settings_show_all,post=True)[0]
            #required_forms = [name_form,phone_form]
            form_list = []
            form_list.append(name_form)
            form_list.append(education_form)
            form_list.append(phone_form)
            form_list.append(work_form)
            form_list.append(address_form)
            all_valid = True
            for form in form_list:
                if not form.is_valid():
                    all_valid = False

            if all_valid:
                for form in form_list:
                    if form.cleaned_data:
                        form.save()
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
def edit_basic(request):
    initial_dict = model_to_dict(request.user)
    name_obj = get_name_obj(request)
    if name_obj:
        initial_dict.update(model_to_dict(name_obj))
    
    if request.method == "POST":
        form = EditAccountForm(request.POST)
        if form.is_valid():
            form.save(request.user)
            return HttpResponseRedirect('?saved=success')
    else:
        form = EditAccountForm(initial=initial_dict)
    
    # Check for the saved query parameter. This powers a save alert on the
    # screen after redirecting.
    saved = request.REQUEST.get('saved')
    if saved:
        if saved=="success":
            message = "Your informatation has been updated."
            message_type = "success"
        else:
            message = "There as an error, please try again."
            message_type = "error"
    else:
        message = ""
        message_type = ""

    ctx = {'form': form,
           'user': request.user,
           'gravatar_100': request.user.get_gravatar_url(size=100),
           'name_obj': name_obj,
           'message':message,
           'messagetype':message_type}
    
    return render_to_response('edit-account.html', ctx,
                              RequestContext(request))

@user_passes_test(User.objects.not_disabled)
def edit_password(request):
    if request.method == "POST":
        form = ChangePasswordForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('?saved=success')
    else:
        form = ChangePasswordForm(user=request.user)
    
    # Check for the saved query parameter. This powers a save alert on the
    # screen after redirecting.
    saved = request.REQUEST.get('saved')
    if saved:
        if saved=="success":
            message = "Your password has been updated."
            message_type = "success"
        else:
            message = "There as an error, please try again."
            message_type = "error"
    else:
        message = ""
        message_type = ""
        
    ctx = {
        'form':form,
        'name_obj': get_name_obj(request),
        'message':message,
        'messagetype':message_type
        }
    return render_to_response('edit-account.html', ctx,
                              RequestContext(request))

@user_passes_test(User.objects.not_disabled)
def edit_delete(request):
    ctx = {'name_obj': get_name_obj(request)}
    return render_to_response('edit-delete.html', ctx,
                              RequestContext(request))

@user_passes_test(User.objects.not_disabled)
def delete_account(request):
    email = request.user.email
    request.user.delete()
    ctx = {'name_obj': get_name_obj(request),'email': email}
    return render_to_response('delete-account-confirmation.html', ctx,
                              RequestContext(request))

@user_passes_test(User.objects.not_disabled)
def disable_account(request):
    user = request.user
    email = user.email
    user.disable()
    logout(request)
    ctx = {'email': email,'name_obj': get_name_obj(request)}
    return render_to_response('disable-account-confirmation.html', ctx,
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
            login_info = details.split(':')
            user = authenticate(username=login_info[0], password=login_info[1])
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
                    received = event['timestamp']
                    EmailLog(email=event['email'], event=event['event'],
                             received=datetime.datetime.fromtimestamp(
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
