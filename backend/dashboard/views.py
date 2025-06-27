from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from core.models import Product, Supplier, Customer, Inbound, Outbound
from audit.models import AuditLog
from django.db.models import Sum
from django.utils.timezone import now, timedelta
from datetime import datetime
from collections import defaultdict
from django.db.models.functions import TruncMonth
from django.db.models import Sum
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from core.models import Inbound, Outbound
from datetime import datetime
import calendar
from users.permissions import IsAdminUser
from django.db import models
# ✅ 19.1 - Admin Dashboard (full stats + audit logs + chart)
class AdminDashboardStatsView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        period = request.GET.get('period', 'monthly')
        
        # Get products that are below their low stock threshold
        low_stock = Product.objects.filter(
            quantity__lte=models.F('low_stock_threshold')
        ).values('name', 'sku', 'quantity', 'low_stock_threshold').order_by('quantity')[:10]

        total_products = Product.objects.count()
        total_customers = Customer.objects.count()
        total_suppliers = Supplier.objects.count()

        recent_inbound = Inbound.objects.select_related('product').order_by('-received_date')[:5].values(
            'product__name', 'quantity', 'received_date'
        )
        recent_outbound = Outbound.objects.select_related('product').order_by('-dispatch_date')[:5].values(
            'product__name', 'quantity', 'dispatch_date'
        )

        # Handle different periods
        if period == 'daily':
            # Last 7 days
            months = []
            for i in range(6, -1, -1):
                day = now().date() - timedelta(days=i)
                months.append(day.strftime("%Y-%m-%d"))
        else:
            # Last 6 months (default)
            months = []
            for i in range(5, -1, -1):
                month = now().date().replace(day=1) - timedelta(days=30 * i)
                months.append(month.strftime("%Y-%m"))

        inbound_data = []
        outbound_data = []

        for m in months:
            if period == 'daily':
                # For daily, filter by exact date match
                try:
                    # Convert string to date object
                    date_obj = datetime.strptime(m, "%Y-%m-%d").date()
                    inbound_count = Inbound.objects.filter(received_date=date_obj).aggregate(total=Sum('quantity'))['total'] or 0
                    outbound_count = Outbound.objects.filter(dispatch_date=date_obj).aggregate(total=Sum('quantity'))['total'] or 0
                except ValueError:
                    inbound_count = 0
                    outbound_count = 0
            else:
                # For monthly, filter by year and month
                try:
                    year, month = m.split('-')
                    inbound_count = Inbound.objects.filter(
                        received_date__year=int(year),
                        received_date__month=int(month)
                    ).aggregate(total=Sum('quantity'))['total'] or 0
                    outbound_count = Outbound.objects.filter(
                        dispatch_date__year=int(year),
                        dispatch_date__month=int(month)
                    ).aggregate(total=Sum('quantity'))['total'] or 0
                except (ValueError, IndexError):
                    inbound_count = 0
                    outbound_count = 0
            
            inbound_data.append(inbound_count)
            outbound_data.append(outbound_count)

        audit_logs = AuditLog.objects.order_by('-timestamp')[:10].values('user__username', 'action', 'object_repr', 'timestamp')

        return Response({
            'low_stock': list(low_stock),
            'totals': {
                'products': total_products,
                'customers': total_customers,
                'suppliers': total_suppliers,
            },
            'recent_inbound': list(recent_inbound),
            'recent_outbound': list(recent_outbound),
            'chart': {
                'labels': months,
                'inbound': inbound_data,
                'outbound': outbound_data,
            },
            'audit_logs': list(audit_logs)
        })


# ✅ Your existing stats view
class DashboardStatsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        products_count = Product.objects.count()
        inbound_total = Inbound.objects.aggregate(total=Sum('quantity'))['total'] or 0
        outbound_total = Outbound.objects.aggregate(total=Sum('quantity'))['total'] or 0

        return Response({
            'products': products_count,
            'inbound': inbound_total,
            'outbound': outbound_total,
        })


# ✅ Your existing 7-day chart view
class DashboardChartView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Group by month name
        inbound_qs = (
            Inbound.objects
            .annotate(month=TruncMonth('received_date'))
            .values('month')
            .annotate(total=Sum('quantity'))
            .order_by('month')
        )

        outbound_qs = (
            Outbound.objects
            .annotate(month=TruncMonth('dispatch_date'))
            .values('month')
            .annotate(total=Sum('quantity'))
            .order_by('month')
        )

        month_set = set()
        inbound_data = {}
        outbound_data = {}

        for entry in inbound_qs:
            month_label = entry['month'].strftime('%b')
            inbound_data[month_label] = entry['total']
            month_set.add(month_label)

        for entry in outbound_qs:
            month_label = entry['month'].strftime('%b')
            outbound_data[month_label] = entry['total']
            month_set.add(month_label)

        # Sort months in calendar order
        all_months = list(calendar.month_abbr)[1:]  # ['Jan', ..., 'Dec']
        labels = [m for m in all_months if m in month_set]

        inbound = [inbound_data.get(m, 0) for m in labels]
        outbound = [outbound_data.get(m, 0) for m in labels]

        return Response({
            "labels": labels,
            "inbound": inbound,
            "outbound": outbound,
        })


# ✅ Your existing latest activities view
class DashboardActivityView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        latest_inbounds = Inbound.objects.select_related('product', 'supplier').order_by('-id')[:5]
        latest_outbounds = Outbound.objects.select_related('product', 'customer').order_by('-id')[:5]

        inbound_list = [{
            'timestamp': i.received_date.strftime('%Y-%m-%d'),
            'user': i.supplier.name if i.supplier else 'System',
            'action': 'Inbound',
            'details': f"{i.quantity} x {i.product.name}"
        } for i in latest_inbounds]

        outbound_list = [{
            'timestamp': o.dispatch_date.strftime('%Y-%m-%d'),
            'user': o.customer.name if o.customer else 'System',
            'action': 'Outbound',
            'details': f"{o.quantity} x {o.product.name}"
        } for o in latest_outbounds]

        return Response(inbound_list + outbound_list)

