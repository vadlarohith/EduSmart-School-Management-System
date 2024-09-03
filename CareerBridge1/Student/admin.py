from django.contrib import admin
from . import models

class FeeDetailsPreview(admin.ModelAdmin):
    list_display = ('StudentRollNo', 'StudentName', 'TotalFee', 'Due')

admin.site.register(models.FeeDetails, FeeDetailsPreview)

class FeeHistoryPreview(admin.ModelAdmin):
    list_display = ('StudentRollNo', 'StudentName', 'TotalFee', 'Due','LatestPaidFee','TransactionNo','Date')

admin.site.register(models.TransactionHistory, FeeHistoryPreview)