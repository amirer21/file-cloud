from django.contrib import admin
from .models import VisitorLog

@admin.register(VisitorLog)
class VisitorLogAdmin(admin.ModelAdmin):
    list_display = ('ip_address', 'user_agent', 'visit_time')
    search_fields = ('ip_address', 'user_agent')
    list_filter = ('visit_time',)
