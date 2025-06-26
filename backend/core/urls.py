from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SupplierViewSet, CustomerViewSet, ProductViewSet  # ✅ include ProductViewSet

router = DefaultRouter()
router.register(r'suppliers', SupplierViewSet)
router.register(r'customers', CustomerViewSet)
router.register(r'products', ProductViewSet, basename='product')  # ✅ register product route

urlpatterns = router.urls
