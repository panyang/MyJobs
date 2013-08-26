import base64
import datetime
import json
import logging
import urllib2

from django.contrib.auth import authenticate, logout
from django.contrib.auth.decorators import user_passes_test
from django.core.mail import EmailMessage
from django.forms.models import model_to_dict
from django.http import HttpResponse, Http404
from django.template import RequestContext
from django.shortcuts import render_to_response, redirect
from django.utils.html import mark_safe
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView

from jira.client import JIRA

from captcha.fields import ReCaptchaField

from secrets import RECAPTCHA_PUBLIC_KEY, RECAPTCHA_PRIVATE_KEY, EMAIL_TO_ADMIN
from secrets import options, my_agent_auth

from myjobs.decorators import user_is_allowed
from myjobs.models import User, EmailLog
from myjobs.forms import *
from myjobs.helpers import *
from myjobs.templatetags.common_tags import get_name_obj
from registration.forms import *

logger = logging.getLogger('__name__')


class About(TemplateView):
    template_name = "about.html"


class Privacy(TemplateView):
    template_name = "privacy-policy.html"


class Terms(TemplateView):
    template_name = "terms.html"


class CaptchaForm(Form):
    captcha = ReCaptchaField(label="", attrs={'theme': 'white'})


def home(request):
    """
    The home page view receives 2 separate Ajax requests, one for the
    registration form and another for the initial profile information form. If
    everything checks out alright and the form saves with no errors, it returns
    a simple string, 'valid', as an HTTP Response, which the front end
    recognizes as a signal to continue with the account creation process. If an
    error occurs, this triggers the jQuery to update the page. The form
    instances with errors must be passed back to the form template it was
    originally from.

    """

    # TODO - rename using snake case
    registrationform = RegistrationForm(auto_id=False)
    loginform = CustomAuthForm(auto_id=False)

    name_form = InitialNameForm(prefix="name")
    education_form = InitialEducationForm(prefix="edu")
    phone_form = InitialPhoneForm(prefix="ph")
    work_form = InitialWorkForm(prefix="work")
    address_form = InitialAddressForm(prefix="addr")

    data_dict = {'registrationform': registrationform,
                 'loginform': loginform,
                 'name_form': name_form,
                 'phone_form': phone_form,
                 'address_form': address_form,
                 'work_form': work_form,
                 'education_form': education_form}

    if request.method == "POST":
        if request.POST.get('action') == "register":
            registrationform = RegistrationForm(request.POST, auto_id=False)
            if registrationform.is_valid():
                new_user, created = User.objects.create_inactive_user(
                    **registrationform.cleaned_data)
                user_cache = authenticate(
                    username=registrationform.cleaned_data['email'],
                    password=registrationform.cleaned_data['password1'])
                expire_login(request, user_cache)
                # pass in gravatar url once user is logged in. Image generated
                # on AJAX success
                data = {'gravatar_url': new_user.get_gravatar_url(size=100)}
                return HttpResponse(json.dumps(data))
            else:
                return HttpResponse(json.dumps(
                    {'errors': registrationform.errors.items()}))

        elif request.POST.get('action') == "login":
            loginform = CustomAuthForm(data=request.POST)
            if loginform.is_valid():
                expire_login(request, loginform.get_user())
                try:
                    url = request.environ.get('HTTP_REFERER')
                    url = url.split('=')
                    url = urllib2.unquote(url[1])
                except:
                    url = 'undefined'
                response_data = {'validation': 'valid', 'url': url}
                return HttpResponse(json.dumps(response_data))
            else:
                return HttpResponse(json.dumps({'errors':
                                                loginform.errors.items()}))

        elif request.POST.get('action') == "save_profile":
            name_form = InitialNameForm(request.POST, prefix="name",
                                        user=request.user)
            education_form = InitialEducationForm(request.POST, prefix="edu",
                                                  user=request.user)
            phone_form = InitialPhoneForm(request.POST, prefix="ph",
                                          user=request.user)
            work_form = InitialWorkForm(request.POST, prefix="work",
                                        user=request.user)
            address_form = InitialAddressForm(request.POST, prefix="addr",
                                              user=request.user)

            forms = [name_form, education_form, phone_form, work_form,
                     address_form]
            valid_forms = [form for form in forms if form.is_valid()]
            invalid_forms = []
            for form in forms:
                if form.changed_data and not form.is_valid():
                    invalid_forms.append(form)

            if not invalid_forms:
                for form in valid_forms:
                    if form.changed_data:
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


def contact(request):
    if request.POST:
        name = request.POST.get('name')
        contact_type = request.POST.get('type')
        reason = request.POST.get('reason')
        from_email = request.POST.get('email')
        phone_num = request.POST.get('phone')
        comment = request.POST.get('comment')
        form = CaptchaForm(request.POST)
        if form.is_valid():
            try:
                jira = JIRA(options=options, basic_auth=my_agent_auth)
            except:
                jira = []
            if not jira:
                msg_subject = ('Contact My.jobs by a(n) %s' % contact_type)
                message = """
                          Name: %s
                          Is a(n): %s
                          Email: %s

                          %s
                          """ % (name, contact_type, from_email, comment)
                to_email = [EMAIL_TO_ADMIN]
                msg = EmailMessage(msg_subject, message, from_email, to_email)
                msg.send()
                return HttpResponse('success')
            else:
                issue_dict = {
                    'project': {'key': 'MJA'},
                    'summary': '%s - %s' % (reason, from_email),
                    'description': '%s' % comment,
                    'issuetype': {'name': 'Task'},
                    'components': [{'id': '12703'}],
                    'customfield_10400': str(name),
                    'customfield_10401': str(from_email),
                    'customfield_10402': str(phone_num),
                }
                jira.create_issue(fields=issue_dict)
                time = datetime.datetime.now().strftime('%A, %B %d, %Y %l:%M %p')
                return HttpResponse(json.dumps({'validation': 'success',
                                                'name': name,
                                                'c_type': contact_type,
                                                'reason': reason,
                                                'c_email': from_email,
                                                'phone': phone_num,
                                                'comment': comment,
                                                'c_time': time}))
        else:
            return HttpResponse(json.dumps({'validation': 'failed',
                                            'errors': form.errors.items()}))
    else:
        form = CaptchaForm()
        data_dict = {'form': form}
    return render_to_response('contact.html', data_dict,
                              RequestContext(request))


@user_is_allowed()
@user_passes_test(User.objects.not_disabled)
def edit_account(request):
    initial_dict = check_name_obj(request.user)
    ctx = {'user': request.user,
           'gravatar_100': request.user.get_gravatar_url(size=100)}

    if request.user.password_change:
        ctx['form'] = ChangePasswordForm(user=request.user)
        ctx['section_name'] = 'password'
    else:
        form = EditAccountForm(initial=initial_dict, user=request.user)
        if request.method == "POST":
            form = EditAccountForm(user=request.user, data=request.POST)
            if form.is_valid():
                form.save(request.user)
                return HttpResponse('success')
        ctx['form'] = form
        ctx['section_name'] = 'basic'

    return render_to_response('myjobs/edit-account.html', ctx,
                              RequestContext(request))


@user_passes_test(User.objects.not_disabled)
def edit_basic(request):
    initial_dict = check_name_obj(request.user)
    form = EditAccountForm(initial=initial_dict, user=request.user)
    if request.method == "POST":
        form = EditAccountForm(user=request.user,
                               data=request.POST,
                               auto_id=False)
        if form.is_valid():
            form.save(request.user)
            return HttpResponse('success')
        else:
            return HttpResponse(json.dumps({'errors': form.errors.items()}))

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
        else:
            return HttpResponse(json.dumps({'errors': form.errors.items()}))

    ctx = {'form': form,
           'section_name': 'password'}
    return render_to_response('myjobs/edit-form-template.html', ctx,
                              RequestContext(request))


@user_passes_test(User.objects.not_disabled)
def edit_delete(request):
    ctx = {'gravatar_150': request.user.get_gravatar_url(size=150)}
    return render_to_response('myjobs/edit-delete.html', ctx,
                              RequestContext(request))


@user_passes_test(User.objects.not_disabled)
def edit_disable(request):
    ctx = {'gravatar_150': request.user.get_gravatar_url(size=150)}
    return render_to_response('myjobs/edit-disable.html', ctx,
                              RequestContext(request))


@user_passes_test(User.objects.not_disabled)
def delete_account(request):
    email = request.user.email
    request.user.delete()
    ctx = {'email': email}
    return render_to_response('myjobs/delete-account-confirmation.html', ctx,
                              RequestContext(request))


@user_passes_test(User.objects.not_disabled)
def disable_account(request):
    user = request.user
    email = user.email
    user.disable()
    logout(request)
    ctx = {'email': email}
    return render_to_response('myjobs/disable-account-confirmation.html', ctx,
                              RequestContext(request))


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
            # login_info is intended to be a base64-encoded string in the
            # format "email:password" where email is a urlquoted string
            login_info = base64.b64decode(details).split(':')
            if len(login_info) == 2:
                login_info[0] = urllib2.unquote(login_info[0])
                user = authenticate(email=login_info[0],
                                    password=login_info[1])
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
                                 )).save()
                    return HttpResponse(status=200)
    return HttpResponse(status=403)


@user_is_allowed(pass_user=True)
def continue_sending_mail(request, user=None):
    """
    Updates the user's last response time to right now.
    Allows the user to choose to continue receiving emails if they are
    inactive.
    """
    user = user or request.user
    user.last_response = datetime.date.today()
    user.save()
    return redirect('/')


def check_name_obj(user):
    """
    Utility function to process and return the user name obect.

    Inputs:
    :user:  request.user object

    Returns:
    :initial_dict: Dictionary object with updated name information
    """
    initial_dict = model_to_dict(user)
    name = get_name_obj(user)
    if name:
        initial_dict.update(model_to_dict(name))
    return initial_dict


@user_is_allowed(pass_user=True)
def unsubscribe_all(request, user=None):
    user = user or request.user
    user.opt_in_myjobs = False
    user.save()

    return render_to_response('myjobs/unsubscribe_all.html',
                              context_instance=RequestContext(request))
