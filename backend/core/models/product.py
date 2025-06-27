from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=100)
    sku = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=50, blank=True)
    tags = models.CharField(max_length=100, blank=True)
    quantity = models.IntegerField(default=0)
    low_stock_threshold = models.IntegerField(default=10)
    is_archived = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} ({self.sku})"

    def save(self, *args, **kwargs):
        # Check if quantity is being reduced and might trigger threshold breach
        if not self._state.adding:  # Not a new instance
            try:
                old_instance = Product.objects.get(pk=self.pk)
                old_quantity = old_instance.quantity
                
                # Check if we're going below threshold
                if (old_quantity > self.low_stock_threshold and 
                    self.quantity <= self.low_stock_threshold and 
                    self.quantity > 0):
                    # Trigger webhook for threshold breach
                    from core.services.webhook_service import WebhookEvents
                    WebhookEvents.inventory_threshold_breach(
                        self, self.quantity, self.low_stock_threshold
                    )
            except Product.DoesNotExist:
                pass
        
        super().save(*args, **kwargs)
