from django.contrib import admin
from django.contrib.auth.models import Group

from myjobs.models import User
from registration.models import ActivationProfile

class UserAdmin(admin.ModelAdmin):
    list_display = ['email','date_joined','last_response','is_active']
    search_fields = ['email']
    list_filter = ['is_active','is_disabled','is_superuser','is_staff']

admin.site.register(User, UserAdmin)
admin.site.register(ActivationProfile)
