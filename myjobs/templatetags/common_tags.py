from django import template

from myjobs import version
from myprofile.models import ProfileUnits

register=template.Library()

@register.simple_tag
def cache_buster():
    cache_buster = "?v=%s" % version.cache_buster
    return cache_buster

@register.filter
def get_name_obj_or_email(user):
    """
    Retrieve the given user's primary name (if one exists and is not blank) or
    email address

    Inputs:
    :user: User instance

    Outputs:
    :name: Name instance or email address
    """
    try:
        name = user.profileunits_set.get(content_type__name="name",
                                         name__primary=True).name
        if not name.get_full_name():
            name = user.email
    except ProfileUnits.DoesNotExist:
        name = user.email
    return name
