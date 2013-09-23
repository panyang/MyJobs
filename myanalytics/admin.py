from django.contrib import admin
from django.contrib.auth.models import Group

from myanalytics.models import SiteViewer, SiteView, UserAgent

admin.site.register(SiteViewer)
admin.site.register(SiteView)
admin.site.register(UserAgent)
