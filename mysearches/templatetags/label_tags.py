from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter(name='make_active_label')
def make_active_label(active, extra_classes=''):
    """
    Creates a Bootstrap label in green or gray

    Inputs:
    :active: flag; True: green label; False: gray label
    :extra_classes: optional string containing custom classes
        for the label; pull-left, pull-right, etc

    Outputs:
    :label: safe HTML string representing a Bootstrap label
    """
    div = '<div class="label label-%s %s">%s</div>'
    if active == True:
        div %= ('success', extra_classes, 'Active')
    else:
        div %= ('default', extra_classes, 'Inactive')
    return mark_safe(div)
