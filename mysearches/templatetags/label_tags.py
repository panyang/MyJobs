from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter(name='make_active_label')
def make_active_label(active, extra_classes=''):
    div = '<div class="label label-%s %s">%s</div>'
    if active == True:
        div %= ('success', extra_classes, 'Active')
    else:
        div %= ('default', extra_classes, 'Inactive')
    return mark_safe(div)
