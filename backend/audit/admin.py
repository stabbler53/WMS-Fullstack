from django.contrib import admin
from django.utils.html import format_html
from .models import AuditLog

@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'action', 'object_repr', 'timestamp', 'formatted_timestamp')
    search_fields = ('user__username', 'action', 'object_repr')
    list_filter = ('action', 'timestamp', 'user')
    ordering = ('-timestamp',)
    readonly_fields = ('user', 'action', 'object_repr', 'timestamp')
    list_per_page = 50
    
    fieldsets = (
        ('Audit Information', {
            'fields': ('user', 'action', 'object_repr', 'timestamp')
        }),
    )
    
    def formatted_timestamp(self, obj):
        return obj.timestamp.strftime('%Y-%m-%d %H:%M:%S')
    formatted_timestamp.short_description = 'Time'
    
    def has_add_permission(self, request):
        return False  # Audit logs should only be created by the system
    
    def has_change_permission(self, request, obj=None):
        return False  # Audit logs should not be editable
    
    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser  # Only superusers can delete audit logs
