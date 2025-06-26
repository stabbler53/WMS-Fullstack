from .models import Product, Supplier, Customer, Inbound, Outbound
from .serializers import ProductSerializer, SupplierSerializer, CustomerSerializer, InboundSerializer, OutboundSerializer
from rest_framework import viewsets, permissions
from rest_framework.permissions import IsAuthenticated
# ✅ Product ViewSet
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]

# ✅ Supplier ViewSet
class SupplierViewSet(viewsets.ModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    permission_classes = [permissions.IsAuthenticated]

# ✅ Customer ViewSet
class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [permissions.IsAuthenticated]

# ✅ Inbound ViewSet — no stock logic here!
class InboundViewSet(viewsets.ModelViewSet):
    queryset = Inbound.objects.all()
    serializer_class = InboundSerializer
    permission_classes = [permissions.IsAuthenticated]

# ✅ Outbound ViewSet — stock check handled in model
class OutboundViewSet(viewsets.ModelViewSet):
    queryset = Outbound.objects.all()
    serializer_class = OutboundSerializer
    permission_classes = [permissions.IsAuthenticated]
