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
        name_obj = Name.objects.filter(user=request.user,primary=True)[0]
    except:
        name_obj = None
    return name_obj
