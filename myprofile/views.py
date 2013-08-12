import json
import logging
import re

from django.contrib.auth.decorators import user_passes_test
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404

from myjobs.models import User
from myjobs.helpers import *
from myprofile.models import ProfileUnits

@user_passes_test(User.objects.not_disabled)
def edit_profile(request):
    """
    Main profile view that the user first sees. Ultimately generates the
    following in data_dict:

    :profile_config:    A dictionary of profile units
    :empty_display_names: A list of ProfileUnits that hasn't been made
    """

    user = request.user

    profile_config = user.profileunits_dict()

    empty_units = [model for model in ProfileUnits.__subclasses__()]

    for units in profile_config.itervalues():
        if units[0].__class__ in empty_units:
            del empty_units[empty_units.index(units[0].__class__)]

    empty_display_names = [model.get_verbose_class() for model in empty_units]

    data_dict = {'profile_config': profile_config,
                 'unit_names': empty_display_names,
                 'view_name': 'My Profile'}

    return render_to_response('myprofile/edit_profile.html', data_dict,
                              RequestContext(request))


@user_passes_test(User.objects.not_disabled)
def handle_form(request):
    item_id = request.REQUEST.get('id', 'new')
    module = request.REQUEST.get('module')
    module = module.replace(" ", "")

    item = None
    if item_id != 'new':
        try:
            item = request.user.profileunits_set.get(pk=item_id)
            item = getattr(item, module.lower())
        except ProfileUnits.DoesNotExist:
            # User is trying to access a nonexistent PU
            # or a PU that belongs to someone else
            raise Http404

    try:
        form = globals()[module + 'Form']
    except KeyError:
        # Someone must have manipulated request data?
        raise Http404

    data_dict = {'view_name': 'My Profile',
                 'item_id': item_id,
                 'module': module}

    if request.method == 'POST':
        if request.POST.get('action') == 'updateEmail':
            activation = ActivationProfile.objects.get_or_create(user=request.user, email=item.email)[0]
            activation.send_activation_email(primary=False)
            return HttpResponse('success')

        if item_id == 'new':
            form_instance = form(user=request.user, data=request.POST, auto_id=False)
        else:
            form_instance = form(user=request.user, instance=item, auto_id=False, data=request.POST)
        model = form_instance._meta.model
        data_dict['form'] = form_instance
        data_dict['verbose'] = model._meta.verbose_name.title()
        if form_instance.is_valid():
            form_instance.save()
            if request.is_ajax():
                return HttpResponse(status=200)
            else:
                return HttpResponseRedirect(reverse('view_profile'))
        else:
            if request.is_ajax():
                return HttpResponse(json.dumps(form_instance.errors))
            else:
                return render_to_response('myprofile/profile_form.html',
                                          data_dict,
                                          RequestContext(request))
    else:
        if item_id == 'new':
            form_instance = form(user=request.user, auto_id=False)
        else:
            form_instance = form(instance=item, auto_id=False)
            if data_dict['module'] == 'SecondaryEmail':
                data_dict['verified'] = item.verified
        model = form_instance._meta.model
        data_dict['form'] = form_instance
        data_dict['verbose'] = model._meta.verbose_name.title()
        return render_to_response('myprofile/profile_form.html',
                                  data_dict,
                                  RequestContext(request))


@user_passes_test(User.objects.not_disabled)
def delete_item(request, item_id):
    try:
        request.user.profileunits_set.get(id=item_id).delete()
    except ProfileUnits.DoesNotExist:
        pass
    return HttpResponseRedirect(reverse('view_profile'))


@user_passes_test(User.objects.not_disabled)
def get_details(request):
    module_config = {}
    item_id = request.GET.get('id')
    item = get_object_or_404(request.user.profileunits_set,
                             pk=item_id)
    module = item.content_type.model
    item = getattr(item, module)
    model = item.__class__
    module_config['verbose'] = model._meta.verbose_name.title()
    module_config['name'] = module
    module_config['item'] = item
    data_dict = {'module': module_config}
    data_dict['view_name'] = 'My Profile'
    return render_to_response('myprofile/profile_details.html',
                              data_dict, RequestContext(request))
