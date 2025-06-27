from rest_framework import routers
from django.urls import path, include
from .views import (
    UploadCSVView,
)

urlpatterns = [
    path('upload-csv/', UploadCSVView.as_view(), name='upload-csv'),
]
