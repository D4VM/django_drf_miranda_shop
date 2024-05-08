from rest_framework import serializers
from .models import Promo


class PromoSerializer(serializers.ModelSerializer):
    product_data = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Promo
        fields = [
            "id",
            "title",
            "featured_image",
            "product",
            "product_data",
        ]

    def get_product_data(self, obj) -> dict:
        data = {
            "id": obj.product.id,
            "title": obj.product.title,
            "category": obj.product.category,
            "child_category": obj.product.child_category,
            "product_style": obj.product.product_style,
            "barcode": obj.product.barcode,
            "stock": obj.product.stock,
            "price": obj.product.price,
            "discount": obj.product.discount,
            "sale_price": obj.product.get_sale_price(),
            "size": obj.product.size,
            "color": obj.product.color,
        }
        return data
