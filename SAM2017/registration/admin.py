from django.contrib import admin
from . import models


class UserFieldFilter(admin.ModelAdmin):
    fields = ['role']


admin.site.register(models.User, UserFieldFilter)
admin.site.register(models.Role)
