from rest_framework import generics
from rest_framework.parsers import MultiPartParser
from drf_spectacular.utils import extend_schema

from .models import Product, ProductImage
from .serializers import ProductSerializer
from .permisions import IsAdminUserOrReadOnly


@extend_schema(tags=["Продукты"])
class ProductListCreateAPIVIEW(generics.ListCreateAPIView):
    """API для создания и получения списка продуктов.

    Позволяет создавать новые продукты и получать список существующих продуктов.
    """

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    parser_classes = [MultiPartParser]
    permission_classes = (IsAdminUserOrReadOnly,)

    def perform_create(self, serializer):
        """
        Создает продукт и связывает его с изображениями, переданными в запросе.

        Если изображения переданы, создает объекты ProductImage для каждого изображения.
        """
        product_instance = serializer.save()
        image_data = self.request.data.getlist("images", [])
        if image_data:
            for data in image_data:
                ProductImage.objects.create(product=product_instance, image=data)


@extend_schema(tags=["Продукты"])
class ProductRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """API для получения, обновления и удаления конкретного продукта.

    Позволяет получать, обновлять и удалять информацию о конкретном продукте.

    """

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = "pk"
    permission_classes = (IsAdminUserOrReadOnly,)
