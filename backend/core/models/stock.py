from django.db import models
from django.utils import timezone
from django.conf import settings
from core.models.product import Product
from core.models.partner import Supplier, Customer
from .product import Product  # ✅ import Product model

def get_current_date():
    return timezone.now().date()

class Inbound(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.PositiveIntegerField()
    batch_id = models.CharField(max_length=100, blank=True, help_text="Batch identifier for tracking")
    expiry_date = models.DateField(null=True, blank=True, help_text="Expiry date for this batch")
    invoice_number = models.CharField(max_length=100, blank=True)
    invoice_file = models.FileField(upload_to='invoices/', blank=True, null=True)
    received_date = models.DateField(auto_now_add=True)

    def __str__(self):
        batch_info = f" (Batch: {self.batch_id})" if self.batch_id else ""
        return f"Inbound: {self.product.name} ({self.quantity}){batch_info}"

    def save(self, *args, **kwargs):
        is_new = self._state.adding
        super().save(*args, **kwargs)
        if is_new:
            print(f"🔄 Inbound: Increasing stock of {self.product.name} by {self.quantity}")
            self.product.quantity += self.quantity
            self.product.save()
            
            # Create or update batch if batch_id is provided
            if self.batch_id and self.expiry_date:
                from .batch import Batch
                batch, created = Batch.objects.get_or_create(
                    product=self.product,
                    batch_id=self.batch_id,
                    defaults={
                        'quantity': self.quantity,
                        'initial_quantity': self.quantity,
                        'expiry_date': self.expiry_date
                    }
                )
                if not created:
                    # Update existing batch
                    batch.quantity += self.quantity
                    batch.initial_quantity += self.quantity
                    batch.save()
            
            # Trigger webhook for inbound creation
            from core.services.webhook_service import WebhookEvents
            WebhookEvents.inbound_created(self, getattr(self, '_user', None))

class Outbound(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.PositiveIntegerField()
    so_reference = models.CharField(max_length=100, blank=True)
    dispatch_date = models.DateField(default=get_current_date)
    delivery_note_file = models.FileField(upload_to='delivery_notes/', null=True, blank=True)

    def __str__(self):
        return f"Outbound: {self.product.name} ({self.quantity})"

    def save(self, *args, **kwargs):
        is_new = self._state.adding
        if is_new and self.product.quantity < self.quantity:
            raise ValueError("Not enough stock to fulfill outbound transaction.")
        super().save(*args, **kwargs)
        if is_new:
            print(f"🔻 Outbound: Reducing stock of {self.product.name} by {self.quantity}")
            self.product.quantity -= self.quantity
            self.product.save()
            
            # Implement FIFO fulfillment using batches
            self._fulfill_from_batches()

    def _fulfill_from_batches(self):
        """Fulfill outbound using FIFO (First In, First Out) based on expiry dates"""
        from .batch import Batch
        
        remaining_quantity = self.quantity
        batches_used = []
        
        # Get available batches ordered by expiry date (FIFO)
        available_batches = Batch.objects.filter(
            product=self.product,
            quantity__gt=0
        ).order_by('expiry_date', 'created_at')
        
        for batch in available_batches:
            if remaining_quantity <= 0:
                break
                
            # Calculate how much to take from this batch
            quantity_to_take = min(remaining_quantity, batch.quantity)
            
            # Update batch quantity
            batch.quantity -= quantity_to_take
            batch.save()
            
            # Track which batches were used
            batches_used.append({
                'batch_id': batch.batch_id,
                'quantity': quantity_to_take,
                'expiry_date': batch.expiry_date
            })
            
            remaining_quantity -= quantity_to_take
        
        # Store batch fulfillment info (could be extended to a separate model)
        if batches_used:
            print(f"📦 FIFO Fulfillment: Used batches {[b['batch_id'] for b in batches_used]}")
        
        # Trigger webhook for outbound creation
        from core.services.webhook_service import WebhookEvents
        WebhookEvents.outbound_created(self, getattr(self, '_user', None))

class StockReconciliation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    counted_quantity = models.IntegerField()
    discrepancy = models.IntegerField()
    reason = models.TextField()
    reconciled_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.name} - Δ{self.discrepancy} by {self.reconciled_by}"