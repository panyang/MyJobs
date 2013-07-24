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
    
@register.filter(name='readable_boolean')
def readable_boolean(value):
    value_lookup = {
        "True": "Yes",
        "False": "No"
    }
    return value_lookup.get(str(value), value)

@register.simple_tag(name='add_required_label')
def add_required_label(field, *classes):
    if not classes:
        classes = ()
    if field.errors:
        classes += ('label-required',)
    return field.label_tag(attrs={'class': ' '.join(classes)})
