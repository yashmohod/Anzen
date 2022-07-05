from django.contrib import admin

from accounts import models

# Register your models here.
admin.site.register(models.User)
admin.site.register(models.inceident)
admin.site.register(models.incidentReport)
admin.site.register(models.location)
