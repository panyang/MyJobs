from django.contrib import admin

from mysearches.models import SavedSearch

class SavedSearchAdmin(admin.ModelAdmin):
    list_display = ['user', 'url', 'label', 'last_sent']
    search_fields = ['email',]

admin.site.register(SavedSearch, SavedSearchAdmin)
