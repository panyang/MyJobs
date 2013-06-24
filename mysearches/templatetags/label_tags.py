from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.simple_tag(name='make_label')
def make_label(active, extra_classes='', **kwargs):
    """
    Creates a Bootstrap label in one of two colors optionally
    provided by the user (defaults: green, gray)

    Inputs:
    :active: flag; True: success color; False: fail color
    :extra_classes: optional string containing custom classes
        for the label; pull-left, pull-right, etc
    :true: string representing the desired label to be used
        if :active: == True
        Default: "success" - results in green label
    :false: string representing the desired label to be used
        if :active: == False
        Default: "default" - results in gray label
    :true_msg: text for label when :active: == True
        Default: "Active"
    :false_msg: text for label when :active: == False
        Default: "Inactive"

    Outputs:
    :label: safe HTML string representing a Bootstrap label
    """
    true = kwargs.pop('true', 'success')
    true_msg = kwargs.pop('true_msg', 'Active')
    false = kwargs.pop('false', 'default')
    false_msg = kwargs.pop('false_msg', 'Inactive')

    div = '<div class="label label-%s %s">%s</div>'
    if active == True:
        div %= (true, extra_classes, true_msg)
    else:
        div %= (false, extra_classes, false_msg)
    return mark_safe(div)
