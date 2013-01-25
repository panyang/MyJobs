from myprofile.forms import *


def instantiate_profile_forms(request, form_classes, settings, post=False):
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
        name_obj = Name.objects.get(user=request.user,primary=True)
    except (Name.DoesNotExist,TypeError):
        name_obj = None
    return name_obj
