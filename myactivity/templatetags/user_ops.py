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
    
@register.filter(name='update_url_length')
def update_url_length(value):
    """
    Return the netloc of the url instead of the full one in the 
    candidate activity list on employer dashboard
    """
    active_url = value
    
    if active_url.find('//') == -1:
        active_url = '//' + value
    
    updated_url = urlparse(active_url)

    return updated_url.netloc
    


    
