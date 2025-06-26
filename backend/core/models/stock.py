from django.db import models
from django.utils import timezone
from core.models.product import Product
from core.models.partner import Supplier, Customer

class Inbound(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.PositiveIntegerField()
    invoice_number = models.CharField(max_length=100, blank=True)
    invoice_file = models.FileField(upload_to='invoices/', blank=True, null=True)
    received_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Inbound: {self.product.name} ({self.quantity})"

    def save(self, *args, **kwargs):
        is_new = self._state.adding
        super().save(*args, **kwargs)
        if is_new:
            print(f"🔄 Inbound: Increasing stock of {self.product.name} by {self.quantity}")
            self.product.quantity += self.quantity
            self.product.save()

class Outbound(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.PositiveIntegerField()
    so_reference = models.CharField(max_length=100, blank=True)
    dispatch_date = models.DateField(default=timezone.now)
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
