from django.db import models

# Create your models here.
from inventory.models import Product
from core.models import Supplier, Customer


class Inbound(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.PositiveIntegerField()
    invoice_number = models.CharField(max_length=100, blank=True)
    received_date = models.DateField(auto_now_add=True)
    invoice_file = models.FileField(upload_to='invoices/', null=True, blank=True)

    def save(self, *args, **kwargs):
        self.product.quantity += self.quantity
        self.product.save()
        super().save(*args, **kwargs)

class Outbound(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.PositiveIntegerField()
    so_reference = models.CharField(max_length=100, blank=True)
    dispatch_date = models.DateField(auto_now_add=True)
    delivery_note_file = models.FileField(upload_to='delivery_notes/', null=True, blank=True)

    def save(self, *args, **kwargs):
        self.product.quantity -= self.quantity
        self.product.save()
        super().save(*args, **kwargs)