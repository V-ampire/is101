from django.contrib import admin

from companies import models


admin.site.register(models.CompanyProfile)

admin.site.register(models.Position)

admin.site.register(models.Branch)

admin.site.register(models.EmployeeProfile)
