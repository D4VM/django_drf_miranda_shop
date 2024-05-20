from .models import Order, OrderItems
from rest_framework import serializers, generics, views
from drf_spectacular.utils import extend_schema
from typing import Dict, List


# TODO: Invoice Generation as PDF new endpoint for download.


class InvoiceSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField(read_only=True)
    products = serializers.SerializerMethodField(read_only=True)
    order_total_price = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Order
        fields = [
            "id",
            "created_at",
            "paid",
            "order_total_price",
            "user",
            "products",
        ]

    def get_user(self, obj) -> dict:
        data = {
            "id": obj.user.pk,
            "username": obj.user.username,
            "email": obj.user.email,
            "city": obj.user.city,
            "address": obj.user.address,
            "phone": obj.user.phone,
            "admin": obj.user.is_staff,
        }
        return data

    def get_products(self, obj) -> List[Dict]:
        order_items = OrderItems.objects.filter(order=obj)
        serialized_products = []
        for item in order_items:
            serialized_product = {
                "id": item.product.id,
                "title": item.product.title,
                "size": item.product.size,
                "color": item.product.color,
                "quantity": item.quantity,
                "price": item.product.price,
                "sale_price": item.product.price,
                "product_total_price": item.product.price * item.quantity,
            }
            serialized_products.append(serialized_product)
        return serialized_products

    def get_order_total_price(self, obj) -> float:
        total_price = 0
        for item in obj.products.all():
            total_price += item.product.price * item.quantity
        return round(total_price, 2)


@extend_schema(tags=["Инвоис"], description="Выдаёт данные для инвойса")
class InvoiceRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Order.objects.all()
    serializer_class = InvoiceSerializer
    lookup_field = "pk"


order_invoice = InvoiceRetrieveAPIView.as_view()


from django.http import HttpResponse
from rest_framework.views import APIView
from django.template.loader import render_to_string

from weasyprint import HTML


@extend_schema(tags=["Инвоис"], description="Выдаёт PDF")
class GenerateInvoiceAPIView(APIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        # Fetch order data based on order_id
        order = Order.objects.get(pk=pk)

        # Serialize order data
        serializer = InvoiceSerializer(order)

        # Render HTML template with serialized data
        html_string = render_to_string("order/invoice.html", {"order": serializer.data})

        # Create PDF file from HTML string
        html = HTML(string=html_string)
        pdf_file = html.write_pdf()

        # Prepare HTTP response with PDF content
        response = HttpResponse(content_type="application/pdf")
        response["Content-Disposition"] = 'filename="invoice.pdf"'
        response.write(pdf_file)

        return response


download_invoice = GenerateInvoiceAPIView.as_view()
