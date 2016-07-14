from django.contrib import admin
from . import models
# Register your models here.
class DeadlineFilter(admin.ModelAdmin):
    fields = ['date']

admin.site.register(models.Deadline, DeadlineFilter)