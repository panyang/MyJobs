from django.contrib import admin
from django.contrib.auth.models import Group

from myjobs.models import User
from registration.models import ActivationProfile

admin.site.register(User)
admin.site.register(ActivationProfile)
admin.site.unregister(Group)
