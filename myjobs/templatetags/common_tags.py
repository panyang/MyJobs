from django import template

from myjobs import version
from myprofile.models import ProfileUnits

register=template.Library()

@register.simple_tag
def cache_buster():
    cache_buster = "?v=%s" % version.cache_buster
    return cache_buster

@register.filter
def get_name_obj(user):
    """
    Retrieve the given user's primary name (if one exists) or an empty string

    Inputs:
    :user: User instance

    Outputs:
    :name: Name instance or blank
    """
    try:
        name = user.profileunits_set.get(content_type__name="name",
                                         name__primary=True).name
        if not name.get_full_name():
            name = ""
    except ProfileUnits.DoesNotExist:
        name = ""
    return name
