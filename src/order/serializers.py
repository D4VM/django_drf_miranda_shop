from rest_framework import serializers
from .models import Order
from product.serializers import ProductSerializer


class OrderSerializer(serializers.ModelSerializer):
    total_price = serializers.FloatField(read_only=True)
    item_price = serializers.FloatField(read_only=True)
    user_data = serializers.SerializerMethodField(read_only=True)
    product_data = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Order
        fields = (
            'id',
            'user_data',
            'product',
            'product_data',
            'quantity',
            'item_price',
            'total_price',
        )

    def get_user_data(self, obj) -> dict:
        data = {
            'id': obj.user.id,
            'username': obj.user.username,
            'email': obj.user.email,
            'city': obj.user.city,
            'address': obj.user.address,
            'phone': obj.user.phone,
        }
        return data
    def get_product_data(self, obj) -> dict:
        data = {
            'id': obj.product.id,
            'title': obj.product.title,
            'category': obj.product.category,
            'child_category': obj.product.child_category,
            'product_style': obj.product.product_style,
            'barcode': obj.product.barcode,
            'stock': obj.product.stock,
            'price': obj.product.price,
            'discount': obj.product.discount,
            'sale_price': obj.product.get_sale_price(),
            'size': obj.product.size,
            'color': obj.product.color,
        }
        return data
