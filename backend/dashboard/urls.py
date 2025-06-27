from django.urls import path
from .views import (
    DashboardStatsView,
    DashboardChartView,
    DashboardActivityView,
    AdminDashboardStatsView,
)

urlpatterns = [
    path('stats/', DashboardStatsView.as_view()),
    path('chart/', DashboardChartView.as_view()),
    path('activity/', DashboardActivityView.as_view()),
    path('admin-stats/', AdminDashboardStatsView.as_view()),  # ✅ new view for admin
]
