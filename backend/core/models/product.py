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
