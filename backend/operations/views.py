from django.shortcuts import render
from rest_framework import viewsets, permissions, serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import pandas as pd

from inventory.models import Product
from .models import Inbound, Outbound
from .serializers import InboundSerializer, OutboundSerializer
from users.permissions import IsOperatorOrAbove

# ✅ Regular ViewSets for CRUD
class InboundViewSet(viewsets.ModelViewSet):
    queryset = Inbound.objects.all()
    serializer_class = InboundSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        inbound = serializer.save()
        product = inbound.product
        product.quantity += inbound.quantity
        product.save()

class OutboundViewSet(viewsets.ModelViewSet):
    queryset = Outbound.objects.all()
    serializer_class = OutboundSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        outbound = serializer.save()
        product = outbound.product

        if product.quantity < outbound.quantity:
            raise serializers.ValidationError("Not enough stock for outbound transaction.")

        product.quantity -= outbound.quantity
        product.save()

# ✅ CSV Upload API
class UploadCSVView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        file = request.FILES.get('file')
        upload_type = request.data.get('type')  # products / inbound / outbound

        if not file or not upload_type:
            return Response({"error": "Missing file or type"}, status=400)

        try:
            df = pd.read_csv(file)

            if upload_type == "products":
                for _, row in df.iterrows():
                    Product.objects.update_or_create(
                        sku=row["sku"],
                        defaults={
                            "name": row["name"],
                            "quantity": row["quantity"],
                            "low_stock_threshold": row.get("low_stock_threshold", 10)
                        }
                    )
            elif upload_type == "inbound":
                for _, row in df.iterrows():
                    product = Product.objects.get(sku=row["sku"])
                    Inbound.objects.create(product=product, quantity=row["quantity"])
            elif upload_type == "outbound":
                for _, row in df.iterrows():
                    product = Product.objects.get(sku=row["sku"])
                    Outbound.objects.create(product=product, quantity=row["quantity"])
            else:
                return Response({"error": "Invalid type"}, status=400)

            return Response({"status": "Success"}, status=201)

        except Exception as e:
            return Response({"error": str(e)}, status=500)
