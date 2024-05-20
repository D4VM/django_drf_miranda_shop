from rest_framework.serializers import (
    ModelSerializer,
    SerializerMethodField,
    FloatField,
)
from product.models import Product, ProductImage


class ProductSerializer(ModelSerializer):
    images = SerializerMethodField()

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
            "size",
            "color",
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
