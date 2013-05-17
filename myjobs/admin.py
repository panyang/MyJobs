from django.contrib import admin
from django.contrib.auth.models import Group

from myjobs.models import User
from registration.models import ActivationProfile
from mysearches.models import SavedSearch

class SavedSearchAdmin(admin.ModelAdmin):
    list_display = ['user', 'url', 'label', 'last_sent']
    search_fields = ['email',]

admin.site.register(User)
admin.site.register(ActivationProfile)
admin.site.unregister(Group)
admin.site.register(SavedSearch, SavedSearchAdmin)
