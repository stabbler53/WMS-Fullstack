# dashboard/urls.py
from django.urls import path
from .views import DashboardStatsView, DashboardChartView, DashboardActivityView

urlpatterns = [
    path('stats/', DashboardStatsView.as_view()),
    path('chart/', DashboardChartView.as_view()),
    path('activity/', DashboardActivityView.as_view()),
]
