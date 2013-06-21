from django.contrib import admin

from mydashboard.models import (
    Company,
    DashboardModule,
    Microsite,
    Administrators
)

admin.site.register(Company)
admin.site.register(DashboardModule)
admin.site.register(Microsite)
admin.site.register(Administrators)
