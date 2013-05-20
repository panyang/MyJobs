from django import template

register = template.Library()

@register.filter(name='display')
def display(value):
    class_ = ''
    if value:
        class_ = 'password-required'
    return class_
