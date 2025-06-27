import requests
import json
import logging
from django.utils import timezone
from django.conf import settings
from core.models import Webhook, WebhookDelivery
from threading import Thread

logger = logging.getLogger(__name__)

class WebhookService:
    @staticmethod
    def trigger_webhook(webhook_type, payload, user=None):
        """Trigger webhooks for a specific event type"""
        webhooks = Webhook.objects.filter(
            webhook_type=webhook_type,
            is_active=True
        )
        
        for webhook in webhooks:
            # Add metadata to payload
            enhanced_payload = {
                'event_type': webhook_type,
                'timestamp': timezone.now().isoformat(),
                'data': payload
            }
            
            if user:
                enhanced_payload['user'] = {
                    'id': user.id,
                    'username': user.username,
                    'role': user.role
                }
            
            # Send webhook asynchronously
            Thread(
                target=WebhookService._send_webhook,
                args=(webhook, enhanced_payload)
            ).start()
    
    @staticmethod
    def _send_webhook(webhook, payload):
        """Send webhook to the configured URL"""
        try:
            headers = webhook.get_headers()
            
            response = requests.post(
                webhook.url,
                json=payload,
                headers=headers,
                timeout=30
            )
            
            # Record delivery
            WebhookDelivery.objects.create(
                webhook=webhook,
                event_type=payload['event_type'],
                payload=payload,
                response_status=response.status_code,
                response_body=response.text,
                success=response.status_code < 400
            )
            
            if response.status_code >= 400:
                logger.error(f"Webhook failed: {webhook.name} - Status: {response.status_code}")
            else:
                logger.info(f"Webhook sent successfully: {webhook.name}")
                
        except Exception as e:
            logger.error(f"Webhook error: {webhook.name} - {str(e)}")
            
            # Record failed delivery
            WebhookDelivery.objects.create(
                webhook=webhook,
                event_type=payload['event_type'],
                payload=payload,
                success=False,
                error_message=str(e)
            )

class WebhookEvents:
    """Event triggers for different webhook types"""
    
    @staticmethod
    def inventory_threshold_breach(product, current_quantity, threshold):
        """Trigger when inventory falls below threshold"""
        payload = {
            'product_id': product.id,
            'product_name': product.name,
            'product_sku': product.sku,
            'current_quantity': current_quantity,
            'threshold': threshold,
            'breach_type': 'low_stock'
        }
        WebhookService.trigger_webhook('inventory_threshold', payload)
    
    @staticmethod
    def bulk_upload_success(file_name, records_count, user):
        """Trigger when bulk upload is successful"""
        payload = {
            'file_name': file_name,
            'records_count': records_count,
            'upload_type': 'bulk_upload'
        }
        WebhookService.trigger_webhook('bulk_upload', payload, user)
    
    @staticmethod
    def inbound_created(inbound, user):
        """Trigger when inbound is created"""
        payload = {
            'inbound_id': inbound.id,
            'product_id': inbound.product.id,
            'product_name': inbound.product.name,
            'quantity': inbound.quantity,
            'batch_id': inbound.batch_id,
            'expiry_date': inbound.expiry_date.isoformat() if inbound.expiry_date else None,
            'supplier': inbound.supplier.name if inbound.supplier else None,
            'invoice_number': inbound.invoice_number,
            'received_date': inbound.received_date.isoformat()
        }
        WebhookService.trigger_webhook('inbound_created', payload, user)
    
    @staticmethod
    def outbound_created(outbound, user):
        """Trigger when outbound is created"""
        payload = {
            'outbound_id': outbound.id,
            'product_id': outbound.product.id,
            'product_name': outbound.product.name,
            'quantity': outbound.quantity,
            'customer': outbound.customer.name if outbound.customer else None,
            'so_reference': outbound.so_reference,
            'dispatch_date': outbound.dispatch_date.isoformat()
        }
        WebhookService.trigger_webhook('outbound_created', payload, user)
    
    @staticmethod
    def batch_expiring_soon(batch):
        """Trigger when batch is expiring soon"""
        payload = {
            'batch_id': batch.id,
            'product_id': batch.product.id,
            'product_name': batch.product.name,
            'batch_number': batch.batch_id,
            'quantity': batch.quantity,
            'expiry_date': batch.expiry_date.isoformat(),
            'days_until_expiry': batch.days_until_expiry
        }
        WebhookService.trigger_webhook('batch_expiring', payload)
    
    @staticmethod
    def batch_expired(batch):
        """Trigger when batch has expired"""
        payload = {
            'batch_id': batch.id,
            'product_id': batch.product.id,
            'product_name': batch.product.name,
            'batch_number': batch.batch_id,
            'quantity': batch.quantity,
            'expiry_date': batch.expiry_date.isoformat()
        }
        WebhookService.trigger_webhook('batch_expired', payload) 