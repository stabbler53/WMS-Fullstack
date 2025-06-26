from rest_framework import serializers
from operations.models import Inbound, Outbound
from core.models import Product
from core.models import Supplier, Customer
from datetime import datetime

# ✅ Inbound Serializer (fixes datetime vs date)
class InboundSerializer(serializers.ModelSerializer):
    received_date = serializers.SerializerMethodField()

    class Meta:
        model = Inbound
        fields = '__all__'

    def get_received_date(self, obj):
        return obj.received_date if obj.received_date else None  # 👈 Removed .date()


# ✅ Outbound Serializer (with stock validation + date fix)
class OutboundSerializer(serializers.ModelSerializer):
    dispatch_date = serializers.SerializerMethodField()

    class Meta:
        model = Outbound
        fields = '__all__'

    def get_dispatch_date(self, obj):
        return obj.dispatch_date if obj.dispatch_date else None  # 👈 Removed .date()

    def validate(self, data):
        product = data['product']
        if product.quantity < data['quantity']:
            raise serializers.ValidationError("Not enough stock for outbound.")
        return data


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

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

