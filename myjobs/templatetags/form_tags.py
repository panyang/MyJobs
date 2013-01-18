from django import template
from django.db import models
from django.forms.fields import BooleanField

register = template.Library()

@register.assignment_tag
def is_boolean_field(field):
    """
    Takes a form field and determines whether it's a boolean field.

    :Input:
    field - a form field instance
    :Output:
    A boolean True if it's a boolean field and False if it is not
    """
    if type(field.field) == BooleanField:
        return True
    else:
        return False


    
