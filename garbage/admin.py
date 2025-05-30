from django.contrib import admin
from .models import Report

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created_at', 'status', 'latitude', 'longitude')
    list_filter = ('status', 'created_at')
    search_fields = ('user__username',)
