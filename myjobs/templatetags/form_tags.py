from django import template
from django.db import models
from django.forms.fields import BooleanField, TypedChoiceField

register = template.Library()

@register.assignment_tag
def is_boolean_field(field):
    """
    Takes a form field and determines whether it's a boolean field.

    Inputs:
    :field:       a form field instance

    Outputs:
    True if it's a boolean field and False if it is not
    """

    if type(field.field) == BooleanField or type(field.field) == TypedChoiceField:
        return True
    else:
        return False


    
