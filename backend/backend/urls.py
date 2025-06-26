"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/', include('users.urls')),
    path('api/partners/', include('partners.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/products/', include('inventory.urls')),
    path('api/', include('operations.urls')),  # Handles /inbound and /outbound
]
# The above code sets up the URL routing for the Django project, including admin routes and API endpoints for user authentication and various app functionalities.
# It uses the `rest_framework_simplejwt` package for token-based authentication and includes URLs for user management, inventory management, and operations management.
# The `include` function is used to reference the URL configurations of the individual apps (`users`, `inventory`, and `operations`), allowing for modular URL management.
# The `TokenObtainPairView` and `TokenRefreshView` are provided by the `rest_framework_simplejwt` package to handle JWT token generation and refreshing, respectively.
