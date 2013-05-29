from django import template
from myjobs import version

register=template.Library()

@register.simple_tag
def cache_buster():
    cache_buster = "?v=%s" % version.cache_buster
    return cache_buster
