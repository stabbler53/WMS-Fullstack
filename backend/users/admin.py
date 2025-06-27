from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from .models import User

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'role', 'is_active', 'is_staff', 'date_joined', 'last_login')
    search_fields = ('username', 'email', 'role')
    list_filter = ('role', 'is_active', 'is_staff', 'date_joined')
    ordering = ('username',)
    readonly_fields = ('date_joined', 'last_login')
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Role & Permissions', {
            'fields': ('role', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'role'),
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related()
    
    def role_display(self, obj):
        role_colors = {
            'admin': 'danger',
            'manager': 'warning', 
            'operator': 'info'
        }
        color = role_colors.get(obj.role, 'secondary')
        return format_html('<span class="badge badge-{}">{}</span>', color, obj.get_role_display())
    role_display.short_description = 'Role'
