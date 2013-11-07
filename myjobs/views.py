import base64
import datetime
from hashlib import sha1
import hmac
import json
import logging
import urllib2
from urlparse import urlparse

from django.contrib.auth import authenticate, logout
from django.contrib.sessions.models import Session
from django.contrib.auth.decorators import user_passes_test
from django.conf import settings
from django.core.mail import EmailMessage
from django.forms.models import model_to_dict
from django.http import HttpResponse, Http404
from django.template import RequestContext
from django.shortcuts import render_to_response, redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView

from jira.client import JIRA

from captcha.fields import ReCaptchaField

from secrets import RECAPTCHA_PUBLIC_KEY, RECAPTCHA_PRIVATE_KEY, EMAIL_TO_ADMIN
from secrets import options, my_agent_auth

from tastypie.models import ApiKey

from myjobs.decorators import user_is_allowed
from myjobs.models import User, EmailLog
from myjobs.forms import *
from myjobs.helpers import *
from myjobs.templatetags.common_tags import get_name_obj
from myprofile.models import ProfileUnits
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


def error_500(request):
    response = render(request, "500.html")
    response.status_code = 500
    return response


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
    nexturl = request.GET.get('next')
    if nexturl:
        nexturl = urllib2.unquote(nexturl)
        nexturl = urllib2.quote(nexturl)

    data_dict = {'num_modules': len(settings.PROFILE_COMPLETION_MODULES),
                 'registrationform': registrationform,
                 'loginform': loginform,
                 'name_form': name_form,
                 'phone_form': phone_form,
                 'address_form': address_form,
                 'work_form': work_form,
                 'education_form': education_form,
                 'nexturl': nexturl}

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
                response = HttpResponse(json.dumps(data))
                response.set_cookie('myguid', new_user.user_guid,
                                    expires=365*24*60*60, domain='.my.jobs')
                return response
            else:
                return HttpResponse(json.dumps(
                    {'errors': registrationform.errors.items()}))

        elif request.POST.get('action') == "login":
            loginform = CustomAuthForm(data=request.POST)
            if loginform.is_valid():
                expire_login(request, loginform.get_user())

                url = request.POST.get('nexturl')

                # Boolean for activation login page to show initial forms
                # again or not
                has_units = False
                if len(loginform.get_user().profileunits_set.all()) > 0:
                    has_units = True

                response_data = {'validation': 'valid', 'url': url,
                                 'units': has_units,
                                 'gravatar_url': loginform.get_user().get_gravatar_url(size=100)}
                response = HttpResponse(json.dumps(response_data))
                response.set_cookie('myguid', loginform.get_user().user_guid,
                                    expires=365*24*60*60, domain='.my.jobs')
                return response
            else:
                return HttpResponse(json.dumps({'errors':
                                                loginform.errors.items()}))

        elif request.POST.get('action') == "save_profile":
            name_form = InitialNameForm(request.POST, prefix="name",
                                        user=request.user)
            if not name_form.changed_data:
                name_form = InitialNameForm(prefix="name")

            education_form = InitialEducationForm(request.POST, prefix="edu",
                                                  user=request.user)
            if not education_form.changed_data:
                education_form = InitialEducationForm(prefix="edu")

            phone_form = InitialPhoneForm(request.POST, prefix="ph",
                                          user=request.user)
            if not phone_form.changed_data:
                phone_form = InitialPhoneForm(prefix="ph")

            work_form = InitialWorkForm(request.POST, prefix="work",
                                        user=request.user)
            if not work_form.changed_data:
                work_form = InitialWorkForm(prefix="work")

            address_form = InitialAddressForm(request.POST, prefix="addr",
                                              user=request.user)
            if not address_form.changed_data:
                address_form = InitialAddressForm(prefix="addr")

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
                project = jira.project('MJA')
                components = []
                component_ids = {'My.Jobs Error': {'id': '12903'},
                                 'Job Seeker': {'id': '12901'},
                                 'Employer': {'id': '12900'},
                                 'Partner': {'id': '12902'}, }
                if component_ids.get(reason):
                    components.append(component_ids.get(reason))
                components.append(component_ids.get(contact_type))

                issue_dict = {
                    'project': {'key': project.key},
                    'summary': '%s - %s' % (reason, from_email),
                    'description': '%s' % comment,
                    'issuetype': {'name': 'Task'},
                    'customfield_10400': str(name),
                    'customfield_10401': str(from_email),
                    'customfield_10402': str(phone_num), }
                
                issue_dict['components'] = components
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


def toolbar(request):
    user = request.user
    if not user or user.is_anonymous():
        guid = request.COOKIES.get('myguid')
        try:
            user = User.objects.get(user_guid=guid)
        except User.DoesNotExist:
            pass
    if not user or user.is_anonymous():
        data = {"user_fullname": "",
                "user_gravatar": "",
                "employer": ""}
    else:
        try:
            name_obj = user.profileunits_set.get(content_type__name="name",
                                         name__primary=True).name
            name = name_obj.get_full_name()
            if not name_obj.get_full_name():
                name = user.email
        except ProfileUnits.DoesNotExist:
            name = user.email
        employer = (True if user.groups.filter(name='Employer')
                    else False)
        data = {"user_fullname": (("%s..." % name[:17]) if len(name) > 20
                                  else name),
                "user_gravatar": user.get_gravatar_url(),
                "employer": employer}
    callback = request.GET.get('callback', '')
    response = '%s(%s);' % (callback, json.dumps(data))
    response = HttpResponse(response, content_type="text/javascript")
    referer = request.META.get('HTTP_REFERER', '')
    referer = urlparse(referer)
    if referer.netloc.endswith('.jobs') and referer.netloc != 'www.my.jobs':
        max_age = 30 * 24 * 60 * 60
        last_name = request.REQUEST.get('site_name', referer.netloc)
        print last_name
        response.set_cookie(key='lastmicrosite',
                            value='%s://%s' % (referer.scheme, referer.netloc),
                            max_age=max_age,
                            domain='.my.jobs')
        response.set_cookie(key='lastmicrositename',
                            value=last_name,
                            max_age=max_age,
                            domain='.my.jobs')
    return response
