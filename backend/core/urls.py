from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    SupplierViewSet,
    CustomerViewSet,
    ProductViewSet,
    InboundViewSet,
    OutboundViewSet,
    ReconcileStockAPIView,
    BarcodeAPIView,
    BatchViewSet,
    WebhookViewSet,
    WebhookDeliveryViewSet,
)

router = DefaultRouter()
router.register(r'suppliers', SupplierViewSet)
router.register(r'customers', CustomerViewSet)
router.register(r'products', ProductViewSet, basename='product')
router.register(r'batches', BatchViewSet, basename='batch')
router.register(r'webhooks', WebhookViewSet, basename='webhook')
router.register(r'webhook-deliveries', WebhookDeliveryViewSet, basename='webhook-delivery')
router.register(r'inbound', InboundViewSet, basename='inbound')
router.register(r'outbound', OutboundViewSet, basename='outbound')

urlpatterns = [
    path('', include(router.urls)),
    path('reconcile-stock/', ReconcileStockAPIView.as_view(), name='reconcile-stock'),  # ✅ manual stock reconciliation endpoint
    path('barcode/<str:sku>/', BarcodeAPIView.as_view(), name='barcode'),  # ✅ barcode generation endpoint
]
