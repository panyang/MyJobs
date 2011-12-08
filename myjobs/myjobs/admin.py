from django.contrib import admin
from django.contrib.auth.models import User
from app.models import UserProfile


class ShortyOption(admin.ModelAdmin):
    """Default shorty admin defs"""
    list_display('id','short_url', 'from_url', 'to_url', 'created')

admin site.register (Shorty, ShortyOption)
