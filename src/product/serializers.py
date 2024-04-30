from rest_framework.serializers import ModelSerializer, SerializerMethodField, FloatField
from product.models import Product, ProductImage


class ProductSerializer(ModelSerializer):
    images = SerializerMethodField()
    sale_price = FloatField(source="get_sale_price", read_only=True)

    class Meta:
        model = Product
        fields = (
            'id',
            'title',
            'category',
            'child_category',
            'product_style',
            'barcode',
            'stock',
            'price',
            'discount',
            'sale_price',
            'size',
            'color',
            'images',
        )

    def get_images(self, obj) -> list:
        images = ProductImage.objects.filter(product=obj)
        return [image.image.url for image in images]
