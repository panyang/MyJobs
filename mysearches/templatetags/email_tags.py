from django import template

register = template.Library()

@register.filter(name='make_verbose_frequency')
def make_verbose_frequency(value):
    if value == 'D':
        return 'Daily'
    if value == 'W':
        return 'Weekly'
    if value == 'M':
        return 'Monthly'
