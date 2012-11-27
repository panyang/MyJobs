from django.contrib import admin
from django.contrib.auth.models import User
from myjobs.models import UserProfile


class UserProfileInline(admin.TabularInline):
    model = UserProfile
    fk_name = 'user'
    max_num = 1


class UserOption(admin.ModelAdmin):
    """User profiles"""
    inlines = [UserProfileInline]
    list_display = ('id', 'username', 'first_name', 'last_name')

admin.site.unregister(User)
admin.site.register (User, UserOption)
    
