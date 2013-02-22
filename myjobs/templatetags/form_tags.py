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

@register.assignment_tag
def is_select_field(field):
    """
    Takes a form field and determines whether it's a select field.

    Inputs:
    :field:       a form field instance

    Outputs:
    True if it's a boolean field and False if it is not
    """

    if type(field.field) == TypedChoiceField:
        return True
    else:
        return False    

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

@register.assignment_tag
def is_select_field(field):
    """
    Takes a form field and determines whether it's a select field.

    Inputs:
    :field:       a form field instance

    Outputs:
    True if it's a boolean field and False if it is not
    """

    if type(field.field) == TypedChoiceField:
        return True
    else:
        return False    

@register.filter
def make_ordinal_month(integer):
    """
    Takes a form field and determines whether it's a select field.

    Inputs:
    :field:       a form field instance

    Outputs:
    True if it's a boolean field and False if it is not
    """

    if 4 <= integer <= 20 or 24 <= integer <= 30:
        suffix = "th"
    else:
        suffix = ["st", "nd", "rd"][integer % 10 - 1]                
    return str(integer) + suffix
