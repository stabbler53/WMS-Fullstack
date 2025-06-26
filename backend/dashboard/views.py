from django.shortcuts import render

# Create your views here.
# dashboard/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils.timezone import now
from django.db.models import Count, Sum
from core.models import Product, Inbound, Outbound
from audit.models import AuditLog  # If you store logs

from datetime import timedelta

class DashboardStatsView(APIView):
    def get(self, request):
        today = now().date()

        total_products = Product.objects.count()
        low_stock = Product.objects.filter(quantity__lt=10).count()

        inbound_today = Inbound.objects.filter(received_date=today).aggregate(total=Sum('quantity'))['total'] or 0
        outbound_today = Outbound.objects.filter(date=today).aggregate(total=Sum('quantity'))['total'] or 0

        return Response({
            "total_products": total_products,
            "low_stock": low_stock,
            "inbound_today": inbound_today,
            "outbound_today": outbound_today
        })


class DashboardChartView(APIView):
    def get(self, request):
        days = 7
        data = []

        for i in range(days):
            day = now().date() - timedelta(days=i)
            inbound = Inbound.objects.filter(received_date=day).aggregate(total=Sum('quantity'))['total'] or 0
            outbound = Outbound.objects.filter(date=day).aggregate(total=Sum('quantity'))['total'] or 0
            data.append({
                "date": day.strftime("%Y-%m-%d"),
                "inbound": inbound,
                "outbound": outbound,
            })

        return Response(list(reversed(data)))  # Latest day last


class DashboardActivityView(APIView):
    def get(self, request):
        logs = AuditLog.objects.order_by('-timestamp')[:10]
        return Response([
            {
                "user": log.user.username,
                "action": log.action,
                "object": log.object_repr,
                "timestamp": log.timestamp.strftime("%Y-%m-%d %H:%M:%S")
            }
            for log in logs
        ])
