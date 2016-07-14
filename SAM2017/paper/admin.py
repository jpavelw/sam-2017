from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.Paper)
# admin.site.register(models.Notifications)
admin.site.register(models.PCMs_Papers)