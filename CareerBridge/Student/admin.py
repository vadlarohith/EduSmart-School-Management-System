from django.contrib import admin
from . import models

class FeeDetailsPreview(admin.ModelAdmin):
    list_display = ('StudentRollNo', 'StudentName', 'TotalFee', 'Due')

admin.site.register(models.FeeDetails, FeeDetailsPreview)

admin.site.register(models.TransactionHistory, FeeDetailsPreview)