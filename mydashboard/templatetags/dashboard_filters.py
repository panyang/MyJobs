from django import template

from myjobs.models import User
from myprofile.models import ProfileUnits, Name

register=template.Library()

@register.filter(name='get_userid')
def get_userid(value):
    
    user = User.objects.get(email=value)
    user_id = user.id
    return user_id
