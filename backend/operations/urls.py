from rest_framework import routers
from django.urls import path, include
from .views import (
    ProductViewSet,
    SupplierViewSet,
    CustomerViewSet,
    InboundViewSet,
    OutboundViewSet,
    UploadCSVView,
)

router = routers.DefaultRouter()
router.register('products', ProductViewSet)
router.register('suppliers', SupplierViewSet)
router.register('customers', CustomerViewSet)
router.register('inbound', InboundViewSet)
router.register('outbound', OutboundViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('upload-csv/', UploadCSVView.as_view(), name='upload-csv'),
]
