from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=255)
    sku = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    quantity = models.IntegerField(default=0)
    low_stock_threshold = models.IntegerField(default=10)

    def __str__(self):
        return f"{self.name} ({self.sku})"
