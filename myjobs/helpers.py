from datetime import timedelta

from django.contrib import auth

from myprofile.forms import *


def instantiate_profile_forms(request, form_classes, settings, post=False):
    """
    Helper function for building out profile form instances that have the same
    key word arguments. This also sets the prefix key word argument to the model's
    lowercased name, allowing for fields with the same name from different models
    (like country_code) to be on the same form with a different namespace.

    Inputs:
    :request:      a request object
    :form_classes: a list of form classes to be instantiated
    :settings:     a dictionary of various keyword arguments to be passed into
                   each form
    :post:         a boolean for determining whether to include the request's
                   POST data in the fomr instance
    """

    profile_instances = []
    for form_class in form_classes:
        settings['prefix'] = form_class.Meta.model.__name__.lower()
        if post:
            profile_instances.append(form_class(request.POST,**settings))
        else:
            profile_instances.append(form_class(**settings))
    return profile_instances

def login(request, *args, **kwargs):
    if request.method == 'POST':
        print request.POST.get('remember_me')
        print request.POST
        if request.POST.get('remember_me', None):
            # Session expires in 2 weeks (default)
            request.session.set_expiry(None)
        else:
            # Session expires in 900 seconds (5 mins)
            request.session.set_expiry(900)
    return auth.login(request, *args, **kwargs)
