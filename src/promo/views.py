from rest_framework import generics
from rest_framework.parsers import MultiPartParser
from drf_spectacular.utils import extend_schema

from .models import Promo
from .seralizers import PromoSerializer
from .permisions import IsAdminUserOrReadOnly


@extend_schema(tags=["Промо"])
class PromoRetrieveUpdateDestroyAPIVieww(generics.RetrieveUpdateDestroyAPIView):
    queryset = Promo.objects.all()
    serializer_class = PromoSerializer
    permission_classes = (IsAdminUserOrReadOnly,)
    lookup_field = "pk"


promo_details = PromoRetrieveUpdateDestroyAPIVieww.as_view()


@extend_schema(tags=["Промо"])
class PromoListCreateAPIView(generics.ListCreateAPIView):
    queryset = Promo.objects.all()
    serializer_class = PromoSerializer
    permission_classes = (IsAdminUserOrReadOnly,)
    parser_classes = [MultiPartParser]


promo_list = PromoListCreateAPIView.as_view()
