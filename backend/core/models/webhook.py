from django.db import models
from django.utils import timezone
import json

class Webhook(models.Model):
    WEBHOOK_TYPES = [
        ('inventory_threshold', 'Inventory Threshold Breach'),
        ('bulk_upload', 'Bulk Upload Success'),
        ('inbound_created', 'Inbound Created'),
        ('outbound_created', 'Outbound Created'),
        ('batch_expiring', 'Batch Expiring Soon'),
        ('batch_expired', 'Batch Expired'),
    ]
    
    name = models.CharField(max_length=100, help_text="Webhook name for identification")
    url = models.URLField(help_text="Webhook endpoint URL")
    webhook_type = models.CharField(max_length=50, choices=WEBHOOK_TYPES, help_text="Type of event to trigger webhook")
    is_active = models.BooleanField(default=True, help_text="Whether this webhook is active")
    secret_key = models.CharField(max_length=255, blank=True, help_text="Secret key for webhook signature")
    headers = models.JSONField(default=dict, blank=True, help_text="Additional headers to send with webhook")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} ({self.get_webhook_type_display()})"
    
    def get_headers(self):
        """Get headers for webhook request"""
        headers = {
            'Content-Type': 'application/json',
            'User-Agent': 'WMS-Webhook/1.0',
        }
        
        if self.secret_key:
            headers['X-WMS-Signature'] = self.secret_key
        
        # Add custom headers
        headers.update(self.headers)
        return headers

class WebhookDelivery(models.Model):
    webhook = models.ForeignKey(Webhook, on_delete=models.CASCADE, related_name='deliveries')
    event_type = models.CharField(max_length=50)
    payload = models.JSONField()
    response_status = models.IntegerField(null=True, blank=True)
    response_body = models.TextField(blank=True)
    success = models.BooleanField(default=False)
    error_message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        status = "✅" if self.success else "❌"
        return f"{status} {self.webhook.name} - {self.event_type} ({self.created_at})" 