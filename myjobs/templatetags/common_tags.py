from django import template

from myjobs import version
from myprofile.models import ProfileUnits
from myjobs.models import User
from myjobs.helpers import get_completion
from mydashboard.models import CompanyUser
from mymessages.models import Message

from django.db.models.loading import get_model

register=template.Library()

@register.simple_tag
def cache_buster():
    cache_buster = "?v=%s" % version.cache_buster
    return cache_buster

@register.simple_tag
def completion_level(level):
    """
    Determines the color of progress bar that should display.
    
    inputs:
    :level: The completion percentage of a user's profile.
    
    outputs:
    A string containing the bootstrap bar type
    """
    
    return get_completion(level)


@register.simple_tag
def get_description(module):
    """
    Gets the description for a module.

    inputs:
    :module: The module to get the description for.
    
    outputs:
    The description for the module, or an empty string if the module or the
    description doesn't exist.
    """
    
    try:
        model = get_model("myprofile", module)
        return model.module_description if model.module_description else ""
    except Exception:
        return ""


@register.filter
def get_name_obj(user, default=""):
    """
    Retrieve the given user's primary name (if one exists) or a default value

    Inputs:
    :user: User instance
    :default: Return this if no name exists

    Outputs:
    :name: Name instance or :default:
    """
    try:
        name = user.profileunits_set.get(content_type__name="name",
                                         name__primary=True).name
        if not name.get_full_name():
            name = default
    except ProfileUnits.DoesNotExist:
        name = default
    return name

@register.assignment_tag
def is_a_group_member(user, group):
    """ 
    Determines whether or not the user is a member of a group

    Inputs:
    :user: User instance
    :group: String of group being checked for

    Outputs:
    Boolean value indicating whether or not the user is a member of the requested group
    """

    try:
        return User.objects.is_group_member(user, group)
    except ValueError:
        return False

@register.assignment_tag
def get_company_name(user):
    """
    Gets the name of companies associated with a user

    Inputs:
    :user: User instance

    Outputs:
    :company_list: A list of company names, or an empty string if there are no
                   companies associated with the user
    """

    try:
        companies = CompanyUser.objects.filter(user=user)
        company_list = [company.company for company in companies]
        return company_list
    except CompanyUser.DoesNotExist:
        return {}

@register.simple_tag(takes_context=True)
def active_tab(context, view_name):
    """
    Determines whether a tab should be highlighted as the active tab.

    Inputs: 
    :view_name: The name of the view, as a string, for the tab being evaluated. 

    Outputs:
    Either "active" if it's the active tab, or an empty string.
    """
    
    return "active" if context.get('view_name', '') == view_name else ""

@register.simple_tag
def get_gravatar(user, size=20):
    """
    Gets the img or div tag for the gravatar or initials block.
    """
    
    return user.get_gravatar_url(size)

@register.filter(name='get_messages')
def get_messages(user):
    """
    Gets messages associated to the users that are marked as not read.
    """

    return user.messages_unread()
