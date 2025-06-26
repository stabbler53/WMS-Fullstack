from django.urls import path
from .views import UploadCSVView, InboundViewSet, OutboundViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'inbound', InboundViewSet)
router.register(r'outbound', OutboundViewSet)

urlpatterns = router.urls + [
    path('upload_csv/', UploadCSVView.as_view(), name='upload_csv')
]
