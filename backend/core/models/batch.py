from django.db import models
from django.utils import timezone
from .product import Product

class Batch(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='batches')
    batch_id = models.CharField(max_length=100, help_text="Unique batch identifier")
    quantity = models.IntegerField(default=0, help_text="Current quantity in this batch")
    initial_quantity = models.IntegerField(default=0, help_text="Initial quantity when batch was created")
    expiry_date = models.DateField(help_text="Expiry date for this batch")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['product', 'batch_id']
        ordering = ['expiry_date', 'created_at']  # FIFO order
    
    def __str__(self):
        return f"{self.product.name} - Batch {self.batch_id} (Exp: {self.expiry_date})"
    
    @property
    def is_expired(self):
        """Check if batch is expired"""
        return self.expiry_date < timezone.now().date()
    
    @property
    def is_expiring_soon(self):
        """Check if batch expires within 30 days"""
        thirty_days_from_now = timezone.now().date() + timezone.timedelta(days=30)
        return self.expiry_date <= thirty_days_from_now and not self.is_expired
    
    @property
    def days_until_expiry(self):
        """Calculate days until expiry"""
        if self.is_expired:
            return 0
        return (self.expiry_date - timezone.now().date()).days
    
    @property
    def utilization_percentage(self):
        """Calculate how much of the batch has been used"""
        if self.initial_quantity == 0:
            return 0
        return ((self.initial_quantity - self.quantity) / self.initial_quantity) * 100 