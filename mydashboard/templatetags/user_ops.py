
from django import template
from urlparse import urlparse
from myjobs.models import User
from myprofile.models import ProfileUnits, Name

register=template.Library()

@register.filter(name='get_distinct_users')
def get_distinct_users(values):
    # Get list of users who have searches for a specific microsite
    # Prepare structure for the addition of user names
    users = dict((search.user, False) for search in values)

    # Get list of primary names for the above users
    names = Name.objects.filter(user__in=users.keys(), primary=True)
    for name in names:
        # Associate each name with its owning user
        users[name.user] = name.get_full_name()

    return users
    
@register.filter(name='url_domain')
def url_domain(value):
    """        
    Retrieve the given url from the candidate activity and returns a netloc
    version of the url

    Inputs:
    :value: url that candidate has for the saved search

    Outputs:
    :updated_url.netloc: url netloc
    """
    active_url = value
    
    if active_url.find('//') == -1:
        active_url = '//' + value
    
    updated_url = urlparse(active_url)

    return updated_url.netloc
