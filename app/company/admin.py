from django.contrib import admin

from company import models


admin.site.register(models.Company)

admin.site.register(models.Position)

admin.site.register(models.Branch)

admin.site.register(models.Employee)
