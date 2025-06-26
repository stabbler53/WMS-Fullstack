from rest_framework import serializers
from .models import Inbound, Outbound, Supplier, Customer
from operations.models import Inbound, Outbound
from inventory.models import Product
from core.models import Supplier, Customer

class InboundSerializer(serializers.ModelSerializer):
    class Meta:
        model = Inbound
        fields = '__all__'

class OutboundSerializer(serializers.ModelSerializer):
    class Meta:
        model = Outbound
        fields = '__all__'

class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = '__all__'

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'
        
    def validate(self, data):
        product = data['product']
        if product.quantity < data['quantity']:
            raise serializers.ValidationError("Not enough stock for outbound.")
        return data


