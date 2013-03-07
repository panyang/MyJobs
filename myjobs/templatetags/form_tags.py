from django import template
from django.db import models
from django.forms.fields import BooleanField, TypedChoiceField

register = template.Library()

@register.assignment_tag
def is_boolean_field(field):
    return type(field.field) == BooleanField

@register.assignment_tag
def is_select_field(field):
    return type(field.field) == TypedChoiceField
