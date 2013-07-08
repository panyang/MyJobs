from django import template

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
    
@register.filter(name='get_userid')
def get_userid(value):    
    user = User.objects.get(email=value)
    user_id = user.id
    return user_id
    
@register.filter(name='get_gravatar')
def get_gravatar(value):    
    user = User.objects.get(email=value)
    user_gravatar = user.gravatar
    return user_gravatar
    
@register.filter(name='get_candidate_name')
def get_candidate_name(value):   
    
    try:    
        user_id = Name.objects.get(user=value)
        user_name = user_id.given_name + " " + user_id.family_name
        
        
    except Name.DoesNotExist:
        user_name = "Name not Given"    
        
    
    return user_name
    
