from rest_framework.serializers import (
    ModelSerializer,
    SerializerMethodField,
    FloatField,
)
from product.models import Product, ProductImage


class ProductSerializer(ModelSerializer):
    images = SerializerMethodField()
    sale_price = FloatField(source="get_sale_price", read_only=True)

    class Meta:
        model = Product
        fields = (
            "id",
            "title",
            "description",
            "category",
            "child_category",
            "product_style",
            "barcode",
            "stock",
            "price",
            "discount",
            "sale_price",
            "size",
            "color",
            "featured_image",
            "images",
        )

    # def get_images(self, obj) -> list:
    #     images = ProductImage.objects.filter(product=obj)
    #     return [image.image.url for image in images]

    def get_images(self, obj) -> list:
        images = ProductImage.objects.filter(product=obj)
        request = self.context.get("request")
        if request is not None:
            api_url = request.build_absolute_uri("/").rstrip("/")
            media_url = f"{api_url}"
            return [f"{media_url}{image.image.url}" for image in images]
        else:
            return [image.image.url for image in images]
