from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter(name='make_active_label')
def make_active_label(active):
    div = '<div class="label label-%s">%s</div>'
    if active == True:
        div %= ('success', 'Active')
    else:
        div %= ('default', 'Inactive')
    return mark_safe(div)
