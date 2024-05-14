from .models import Order, OrderItems
from rest_framework import serializers, generics
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
                "price": item.product.get_sale_price(),
                "discount": item.product.discount,
                "sale_price": item.product.price,
                "product_total_price": item.product.get_sale_price() * item.quantity,
            }
            serialized_products.append(serialized_product)
        return serialized_products

    def get_order_total_price(self, obj) -> float:
        total_price = 0
        for item in obj.products.all():
            total_price += item.product.get_sale_price() * item.quantity
        return round(total_price, 2)


@extend_schema(tags=["Инвоис"], description="Выдаёт данные для инвойса")
class InvoiceRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Order.objects.all()
    serializer_class = InvoiceSerializer
    lookup_field = "pk"


order_invoice = InvoiceRetrieveAPIView.as_view()
