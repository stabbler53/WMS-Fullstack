from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('admin/', admin.site.urls),

    # ✅ JWT Auth
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # ✅ Users app
    path('api/users/', include('users.urls')),

    # ✅ Core app (products, suppliers, customers)
    path('api/', include('core.urls')),  # Handles /products/, /suppliers/, /customers/

    # ✅ Operations app (inbound, outbound)
    path('api/', include('operations.urls')),  # Handles /inbound/, /outbound/

    path('api/dashboard/', include('dashboard.urls')),
    # ✅ Inventory app (products)
]

# ✅ Serve uploaded media files in dev mode
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
