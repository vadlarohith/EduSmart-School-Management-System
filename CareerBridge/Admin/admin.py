from django.contrib import admin
from . import models

admin.site.register(models.Admin)

admin.site.register(models.Student)

admin.site.register(models.Teacher)

admin.site.register(models.Posters)

admin.site.register(models.TimeTable)
