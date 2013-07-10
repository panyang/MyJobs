from django import template

from myjobs import version
from myprofile.models import ProfileUnits
from myjobs.models import User
from mydashboard.models import CompanyUser

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

@register.assignment_tag
def is_a_group_member(user, group):
    """ 
    Determines whether or not the user is a member of the Employer group

    Inputs:
    :user: User instance
    :group: String of group being checked for

    Outputs:
    Boolean value indicating whether or not the user is a member of the requested group
    """

    return User.objects.is_group_member(user, group)

@register.assignment_tag
def get_company_name(user):
    """
    Gets the name of companies associated with a user

    Inputs:
    :user: User instance

    Outputs:
    :company_list: A list of company names, or an empty string if there are no companies associated with the user
    """

    try:
        company_list = {}
        companies = CompanyUser.objects.filter(user=user)
        for i, company in enumerate(companies):
            company_list[i] = company.company
        return company_list
    except CompanyUser.DoesNotExist:
        return {}
