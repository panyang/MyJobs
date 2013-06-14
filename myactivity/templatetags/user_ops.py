from django import template

from myjobs.models import User
from myprofile.models import ProfileUnits, Name

register=template.Library()

def get_name(user):
    """
    Get the primary name object for the specified user, or 'Name not provided' if none exists

    Inputs:
    :user: User instance
    """
    try:
        name = user.profileunits_set.get(content_type__name='name', name__primary=True).name.get_full_name()
    except (ProfileUnits.DoesNotExist, ProfileUnits.MultipleObjectsReturned):
        name = 'Name not provided'
    return name

@register.filter(name='get_distinct_users')
def get_distinct_users(values):
    # List of users who have searches for a specific microsite
    users = set(search.user for search in values)

    # Full names for each of the previous users
    names = [get_name(user) for user in users]

    # Not everyone has a Name object marked primary - neither of the following will work
    #names = ProfileUnits.objects.filter(content_type__name='name', name__primary=True, user__in=users).order_by('user__email')
    #names = Name.objects.filter(user__in=users, primary=True)

    return zip(users, names)

