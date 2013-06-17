from django import template

from myjobs.models import User
from myprofile.models import ProfileUnits, Name

register=template.Library()

@register.filter(name='get_distinct_users')
def get_distinct_users(values):
    print len(values)
    # Get list of users who have searches for a specific microsite
    # Force queryset to execute
    users = set(search.user for search in values)
    # Prepare structure for the addition of user names
    users = dict((user, False) for user in users)
    print len(users)

    # Get list of primary names for the above users
    names = Name.objects.filter(user__in=users.keys(), primary=True)
    for name in names:
        # Associate each name with its owning user
        users[name.user] = name.get_full_name()

    return users

