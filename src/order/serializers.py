from rest_framework import serializers
from product.models import Product
from .models import Order, OrderItems


class OrderItemSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    price_per_item = serializers.SerializerMethodField(read_only=True)
    product_total_price = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = OrderItems
        fields = [
            "product",
            "quantity",
            "price_per_item",
            "product_total_price",
        ]

    def get_price_per_item(self, obj) -> int:
        return obj.product.get_sale_price()

    def get_product_total_price(self, obj) -> float:
        return obj.quantity * obj.product.get_sale_price()


class OrderSerializer(serializers.ModelSerializer):
    products = OrderItemSerializer(many=True)
    order_total_price = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Order
        fields = [
            "id",
            "created_at",
            "paid",
            "user",
            "order_total_price",
            "products",
        ]

    def get_order_total_price(self, obj) -> float:
        total_price = 0
        for item in obj.products.all():
            total_price += item.product.get_sale_price() * item.quantity
        return total_price

    def create(self, validated_data):
        products_data = validated_data.pop("products")
        order = Order.objects.create(user=validated_data["user"])
        for product_data in products_data:
            OrderItems.objects.create(order=order, **product_data)
        return order
