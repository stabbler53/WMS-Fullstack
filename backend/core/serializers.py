from rest_framework import serializers
from .models import Supplier, Customer, Product, Inbound, Outbound

class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = '__all__'

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class InboundSerializer(serializers.ModelSerializer):
    class Meta:
        model = Inbound
        fields = '__all__'
class OutboundSerializer(serializers.ModelSerializer):
    class Meta:
        model = Outbound
        fields = '__all__'

    def validate(self, data):
        product = data['product']  # Already a Product instance
        if product.quantity < data['quantity']:
            raise serializers.ValidationError("Not enough stock for outbound.")
        return data