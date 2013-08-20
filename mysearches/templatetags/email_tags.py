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


@register.filter(name='time_created')
def time_created(savedsearch):
    return savedsearch.created_on.strftime('%A, %B %d, %Y %l:%M %p')