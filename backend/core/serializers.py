from rest_framework import serializers
from .models import (
    Supplier,
    Customer,
    Product,
    Inbound,
    Outbound,
    StockReconciliation,
    Batch,
    Webhook,
    WebhookDelivery
)

# ✅ Supplier Serializer
class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = '__all__'


# ✅ Customer Serializer
class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'


# ✅ Product Serializer
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


# ✅ Batch Serializer
class BatchSerializer(serializers.ModelSerializer):
    is_expired = serializers.ReadOnlyField()
    is_expiring_soon = serializers.ReadOnlyField()
    days_until_expiry = serializers.ReadOnlyField()
    utilization_percentage = serializers.ReadOnlyField()
    
    class Meta:
        model = Batch
        fields = '__all__'


# ✅ Webhook Serializer
class WebhookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Webhook
        fields = '__all__'


# ✅ Webhook Delivery Serializer
class WebhookDeliverySerializer(serializers.ModelSerializer):
    webhook_name = serializers.CharField(source='webhook.name', read_only=True)
    
    class Meta:
        model = WebhookDelivery
        fields = '__all__'


# ✅ Inbound Serializer with batch support
class InboundSerializer(serializers.ModelSerializer):
    class Meta:
        model = Inbound
        fields = '__all__'


# ✅ Outbound Serializer with stock validation
class OutboundSerializer(serializers.ModelSerializer):
    class Meta:
        model = Outbound
        fields = '__all__'

    def validate(self, data):
        product = data['product']
        requested_qty = data['quantity']
        if product.quantity < requested_qty:
            raise serializers.ValidationError("Not enough stock for outbound.")
        return data


# ✅ Stock Reconciliation Serializer
class StockReconciliationSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockReconciliation
        fields = '__all__'
