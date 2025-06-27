from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import Product, Supplier, Customer, Inbound, Outbound, StockReconciliation, Batch, Webhook, WebhookDelivery

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'sku', 'category', 'quantity', 'low_stock_threshold', 'stock_status', 'is_archived')
    search_fields = ('name', 'sku', 'category')
    list_filter = ('category', 'is_archived')
    ordering = ('name',)
    list_editable = ('low_stock_threshold', 'is_archived')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'sku', 'description', 'category')
        }),
        ('Stock Information', {
            'fields': ('quantity', 'low_stock_threshold')
        }),
        ('Additional Information', {
            'fields': ('tags', 'is_archived'),
            'classes': ('collapse',)
        }),
    )
    
    def stock_status(self, obj):
        if obj.quantity <= obj.low_stock_threshold:
            return format_html('<span style="color: red;">⚠️ Low Stock</span>')
        elif obj.quantity == 0:
            return format_html('<span style="color: red;">❌ Out of Stock</span>')
        else:
            return format_html('<span style="color: green;">✅ In Stock</span>')
    stock_status.short_description = 'Stock Status'

@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone')
    search_fields = ('name', 'email')
    ordering = ('name',)
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name',)
        }),
        ('Contact Information', {
            'fields': ('email', 'phone')
        }),
    )

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone')
    search_fields = ('name', 'email')
    ordering = ('name',)
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name',)
        }),
        ('Contact Information', {
            'fields': ('email', 'phone')
        }),
    )

@admin.register(Inbound)
class InboundAdmin(admin.ModelAdmin):
    list_display = ('product', 'supplier', 'quantity', 'batch_id', 'expiry_date', 'received_date', 'invoice_number')
    search_fields = ('product__name', 'supplier__name', 'invoice_number', 'batch_id')
    list_filter = ('received_date', 'supplier', 'product')
    ordering = ('-received_date',)
    readonly_fields = ('received_date',)
    
    fieldsets = (
        ('Transaction Information', {
            'fields': ('product', 'supplier', 'quantity')
        }),
        ('Batch Information', {
            'fields': ('batch_id', 'expiry_date')
        }),
        ('Documentation', {
            'fields': ('invoice_number', 'invoice_file')
        }),
        ('System Information', {
            'fields': ('received_date',),
            'classes': ('collapse',)
        }),
    )

@admin.register(Outbound)
class OutboundAdmin(admin.ModelAdmin):
    list_display = ('product', 'customer', 'quantity', 'dispatch_date', 'so_reference')
    search_fields = ('product__name', 'customer__name', 'so_reference')
    list_filter = ('dispatch_date', 'customer', 'product')
    ordering = ('-dispatch_date',)
    
    fieldsets = (
        ('Transaction Information', {
            'fields': ('product', 'customer', 'quantity')
        }),
        ('Documentation', {
            'fields': ('so_reference', 'dispatch_date', 'delivery_note_file')
        }),
    )

@admin.register(StockReconciliation)
class StockReconciliationAdmin(admin.ModelAdmin):
    list_display = ('product', 'counted_quantity', 'discrepancy', 'reason', 'reconciled_by', 'timestamp', 'discrepancy_status')
    search_fields = ('product__name', 'reason', 'reconciled_by__username')
    list_filter = ('timestamp', 'reconciled_by')
    ordering = ('-timestamp',)
    readonly_fields = ('timestamp', 'reconciled_by')
    
    fieldsets = (
        ('Reconciliation Details', {
            'fields': ('product', 'counted_quantity', 'discrepancy')
        }),
        ('Documentation', {
            'fields': ('reason', 'reconciled_by', 'timestamp')
        }),
    )
    
    def save_model(self, request, obj, form, change):
        if not change:  # Only set reconciled_by on creation
            obj.reconciled_by = request.user
        super().save_model(request, obj, form, change)
    
    def discrepancy_status(self, obj):
        if obj.discrepancy > 0:
            return format_html('<span style="color: green;">📈 Surplus</span>')
        elif obj.discrepancy < 0:
            return format_html('<span style="color: red;">📉 Shortage</span>')
        else:
            return format_html('<span style="color: blue;">✅ Balanced</span>')
    discrepancy_status.short_description = 'Status'

@admin.register(Batch)
class BatchAdmin(admin.ModelAdmin):
    list_display = ('product', 'batch_id', 'quantity', 'initial_quantity', 'expiry_date', 'status', 'utilization')
    search_fields = ('batch_id', 'product__name', 'product__sku')
    list_filter = ('expiry_date', 'product__category')
    ordering = ('expiry_date', 'created_at')
    
    fieldsets = (
        ('Batch Information', {
            'fields': ('product', 'batch_id', 'expiry_date')
        }),
        ('Quantity', {
            'fields': ('quantity', 'initial_quantity')
        }),
    )
    
    def status(self, obj):
        if obj.is_expired:
            return format_html('<span style="color: red;">🔴 Expired</span>')
        elif obj.is_expiring_soon:
            return format_html('<span style="color: orange;">🟡 Expiring Soon</span>')
        return format_html('<span style="color: green;">🟢 Active</span>')
    status.short_description = 'Status'
    
    def utilization(self, obj):
        return f"{obj.utilization_percentage:.1f}%"
    utilization.short_description = 'Utilization'

@admin.register(Webhook)
class WebhookAdmin(admin.ModelAdmin):
    list_display = ('name', 'webhook_type', 'url', 'is_active', 'created_at')
    search_fields = ('name', 'url')
    list_filter = ('webhook_type', 'is_active', 'created_at')
    ordering = ('-created_at',)
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'url', 'webhook_type')
        }),
        ('Configuration', {
            'fields': ('is_active', 'secret_key', 'headers')
        }),
    )

@admin.register(WebhookDelivery)
class WebhookDeliveryAdmin(admin.ModelAdmin):
    list_display = ('webhook', 'event_type', 'response_status', 'success', 'created_at')
    search_fields = ('webhook__name', 'event_type')
    list_filter = ('success', 'event_type', 'created_at')
    ordering = ('-created_at',)
    readonly_fields = ('webhook', 'event_type', 'payload', 'response_status', 'response_body', 'success', 'error_message', 'created_at')
    
    fieldsets = (
        ('Delivery Information', {
            'fields': ('webhook', 'event_type', 'success')
        }),
        ('Request/Response', {
            'fields': ('payload', 'response_status', 'response_body', 'error_message')
        }),
        ('Timing', {
            'fields': ('created_at',)
        }),
    )
    
    def has_add_permission(self, request):
        return False  # Webhook deliveries are created automatically
