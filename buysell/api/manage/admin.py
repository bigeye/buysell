from django.contrib import admin
from buysell.api.manage.models import Report, Log

class ReportAdmin(admin.ModelAdmin):
    model = Report

class LogAdmin(admin.ModelAdmin):
    model = Log

admin.site.register(Report, ReportAdmin)
admin.site.register(Log, LogAdmin)
