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

    form_classes = [InitialNameForm,EducationForm,PhoneForm,EmploymentForm,AddressForm]
    # Parameters passed into the form class. See forms.py in myprofile
    # for more detailed docs
    settings = {'auto_id':False, 'empty_permitted':True, 'only_show_required':True,
                'user': request.user}
    settings_show_all = {'auto_id':False, 'empty_permitted':True,
                         'only_show_required':False,'user': request.user}
    profile_forms = instantiate_profile_forms(request, form_classes,settings)
    name_form = instantiate_profile_forms(request, [InitialNameForm],settings)[0]
    education_form = instantiate_profile_forms(request,[EducationForm],settings)[0]
    phone_form = instantiate_profile_forms(request, [PhoneForm],settings_show_all)[0]
    work_form = instantiate_profile_forms(request, [EmploymentForm],settings)[0]
    address_form = instantiate_profile_forms(request, [AddressForm],settings)[0]

    data_dict = {'registrationform':registrationform,
                 'loginform': loginform,
                 'profile_forms': profile_forms,
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
            # rebuild the form object with the post parameter = True
            profile_forms =  instantiate_profile_forms(request,form_classes,
                                                       settings,post=True)
            name_form = instantiate_profile_forms(request, [InitialNameForm],
                                                  settings,post=True)[0]
            education_form = instantiate_profile_forms(request,[EducationForm],
                                                       settings,post=True)[0]
            phone_form = instantiate_profile_forms(request, [PhoneForm],
                                                   settings_show_all,post=True)[0]
            work_form = instantiate_profile_forms(request, [EmploymentForm],
                                                  settings,post=True)[0]
            address_form = instantiate_profile_forms(request, [AddressForm],
                                                     settings,post=True)[0]
            all_valid = True
            for form in profile_forms:
                if not form.is_valid():
                    all_valid = False

            if all_valid:
                for form in profile_forms:
                    if form.cleaned_data:
                        form.save()
                return HttpResponse('valid')
            else:
                return render_to_response('includes/initial-profile-form.html',
                                          {'profile_forms': profile_forms,
                                          'name_form': name_form,
                                         'phone_form': phone_form,
                                         'address_form': address_form,
                                         'work_form': work_form,
                                         'education_form': education_form},
                                          context_instance=RequestContext(request))
            
    return render_to_response('index.html', data_dict, RequestContext(request))

    
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


                        
