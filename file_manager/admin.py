from django.contrib import admin
from .models import VisitorLog, UserActionLog

@admin.register(VisitorLog)
class VisitorLogAdmin(admin.ModelAdmin):
    list_display = ('ip_address', 'user_agent', 'visit_time')
    search_fields = ('ip_address', 'user_agent')
    list_filter = ('visit_time',)

@admin.register(UserActionLog)
class UserActionLogAdmin(admin.ModelAdmin):
    list_display = ('ip_address', 'action_time', 'action_type', 'file_names')
    search_fields = ('ip_address', 'file_names', 'action_type')
    list_filter = ('action_time', 'action_type')
