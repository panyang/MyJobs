from django.contrib import admin
from shorty.models import Shorty, Click


class ShortyOption(admin.ModelAdmin):
    """Default shorty admin defs"""
    list_display = ('id', 'created', 'shorty_url', 'from_url', 'to_url')

admin.site.register(Shorty, ShortyOption)
