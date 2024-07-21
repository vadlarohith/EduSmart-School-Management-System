from django.contrib import admin
from . import models

admin.site.register(models.Admin)

class StudentPreview(admin.ModelAdmin):
    list_display = ('FullName','Class','RollNo','MobileNo')

admin.site.register(models.Student, StudentPreview)

admin.site.register(models.Teacher)

admin.site.register(models.Posters)

admin.site.register(models.TimeTable)
