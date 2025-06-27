from core.models import Product, Supplier, Customer, Inbound, Outbound, StockReconciliation, Batch, Webhook, WebhookDelivery

from .serializers import (
    ProductSerializer,
    SupplierSerializer,
    CustomerSerializer,
    InboundSerializer,
    OutboundSerializer,
    BatchSerializer,
    WebhookSerializer,
    WebhookDeliverySerializer,
)

from rest_framework import viewsets, permissions, filters
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from users.permissions import IsAdminUser, IsManagerOrAdmin, IsOperatorOrAbove, ReadOnly
from django.http import HttpResponse
import barcode
from barcode.writer import ImageWriter
from io import BytesIO
import base64
from rest_framework.decorators import action
from django.utils import timezone
from datetime import timedelta

# ✅ Product ViewSet
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.filter(is_archived=False)  # Only show active products
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['category', 'tags', 'sku']
    search_fields = ['name', 'sku', 'tags', 'category', 'description']
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminUser() if self.action == 'destroy' else IsManagerOrAdmin()]
        return [IsOperatorOrAbove()]
    
    def get_queryset(self):
        # Allow admins to see archived products for management
        if self.request.user.role == 'admin':
            return Product.objects.all()
        return Product.objects.filter(is_archived=False)
    
    def perform_destroy(self, instance):
        # Soft delete - archive instead of hard delete
        instance.is_archived = True
        instance.save()
    
    @action(detail=True, methods=['post'])
    def archive(self, request, pk=None):
        product = self.get_object()
        product.is_archived = True
        product.save()
        return Response({'message': 'Product archived successfully'})
    
    @action(detail=True, methods=['post'])
    def unarchive(self, request, pk=None):
        product = self.get_object()
        product.is_archived = False
        product.save()
        return Response({'message': 'Product unarchived successfully'})

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

# ✅ Batch ViewSet
class BatchViewSet(viewsets.ModelViewSet):
    queryset = Batch.objects.all()
    serializer_class = BatchSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['product', 'batch_id', 'expiry_date']
    search_fields = ['batch_id', 'product__name']
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsManagerOrAdmin()]
        return [IsOperatorOrAbove()]
    
    @action(detail=False, methods=['get'])
    def expiring_soon(self, request):
        """Get batches expiring within 30 days"""
        thirty_days_from_now = timezone.now().date() + timedelta(days=30)
        expiring_batches = Batch.objects.filter(
            expiry_date__lte=thirty_days_from_now,
            expiry_date__gte=timezone.now().date(),
            quantity__gt=0
        ).order_by('expiry_date')
        
        serializer = self.get_serializer(expiring_batches, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def expired(self, request):
        """Get expired batches with remaining stock"""
        expired_batches = Batch.objects.filter(
            expiry_date__lt=timezone.now().date(),
            quantity__gt=0
        ).order_by('expiry_date')
        
        serializer = self.get_serializer(expired_batches, many=True)
        return Response(serializer.data)

# ✅ Webhook ViewSet
class WebhookViewSet(viewsets.ModelViewSet):
    queryset = Webhook.objects.all()
    serializer_class = WebhookSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['webhook_type', 'is_active']
    search_fields = ['name', 'url']
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminUser()]
        return [IsManagerOrAdmin()]
    
    @action(detail=True, methods=['post'])
    def test(self, request, pk=None):
        """Test webhook by sending a test payload"""
        webhook = self.get_object()
        
        test_payload = {
            'event_type': 'test',
            'timestamp': timezone.now().isoformat(),
            'data': {
                'message': 'This is a test webhook from WMS',
                'webhook_id': webhook.id,
                'webhook_name': webhook.name
            }
        }
        
        from core.services.webhook_service import WebhookService
        WebhookService._send_webhook(webhook, test_payload)
        
        return Response({'message': 'Test webhook sent successfully'})
    
    @action(detail=True, methods=['post'])
    def toggle_active(self, request, pk=None):
        """Toggle webhook active status"""
        webhook = self.get_object()
        webhook.is_active = not webhook.is_active
        webhook.save()
        
        status = 'activated' if webhook.is_active else 'deactivated'
        return Response({'message': f'Webhook {status} successfully'})

# ✅ Webhook Delivery ViewSet
class WebhookDeliveryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = WebhookDelivery.objects.all()
    serializer_class = WebhookDeliverySerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['webhook', 'event_type', 'success']
    search_fields = ['webhook__name', 'event_type']
    
    def get_permissions(self):
        return [IsManagerOrAdmin()]
    
    @action(detail=False, methods=['get'])
    def recent_failures(self, request):
        """Get recent failed webhook deliveries"""
        failed_deliveries = WebhookDelivery.objects.filter(
            success=False
        ).order_by('-created_at')[:50]
        
        serializer = self.get_serializer(failed_deliveries, many=True)
        return Response(serializer.data)

# ✅ Inbound ViewSet — stock logic handled in model
class InboundViewSet(viewsets.ModelViewSet):
    queryset = Inbound.objects.all()
    serializer_class = InboundSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['product', 'supplier', 'received_date']
    search_fields = ['product__name', 'supplier__name', 'invoice_number']
    
    def get_queryset(self):
        # Only show transactions for active products
        return Inbound.objects.filter(product__is_archived=False)
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsManagerOrAdmin()]
        return [IsOperatorOrAbove()]

# ✅ Outbound ViewSet — stock check handled in model
class OutboundViewSet(viewsets.ModelViewSet):
    queryset = Outbound.objects.all()
    serializer_class = OutboundSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['product', 'customer', 'dispatch_date']
    search_fields = ['product__name', 'customer__name', 'so_reference']
    
    def get_queryset(self):
        # Only show transactions for active products
        return Outbound.objects.filter(product__is_archived=False)
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsManagerOrAdmin()]
        return [IsOperatorOrAbove()]

# ✅ Stock Reconciliation API
class ReconcileStockAPIView(APIView):
    def get_permissions(self):
        if self.request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
            return [IsManagerOrAdmin()]
        return [IsOperatorOrAbove()]

    def post(self, request):
        product_id = request.data.get('product_id')
        counted_qty = int(request.data.get('counted_quantity', 0))
        reason = request.data.get('reason', '')

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found'}, status=404)

        discrepancy = counted_qty - product.quantity

        StockReconciliation.objects.create(
            product=product,
            counted_quantity=counted_qty,
            discrepancy=discrepancy,
            reason=reason,
            reconciled_by=request.user
        )

        product.quantity = counted_qty
        product.save(update_fields=["quantity"])

        return Response({'message': 'Stock reconciled successfully'}, status=200)

# ✅ Barcode Generation API
class BarcodeAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, sku):
        try:
            # Generate Code128 barcode
            code128 = barcode.get('code128', sku, writer=ImageWriter())
            
            # Create image in memory
            buffer = BytesIO()
            code128.write(buffer)
            buffer.seek(0)
            
            # Convert to base64
            image_data = base64.b64encode(buffer.getvalue()).decode()
            
            return Response({
                'barcode': f'data:image/png;base64,{image_data}',
                'sku': sku
            })
        except Exception as e:
            return Response({'error': f'Failed to generate barcode: {str(e)}'}, status=400)
