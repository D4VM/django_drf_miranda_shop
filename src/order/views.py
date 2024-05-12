from rest_framework import generics
from .models import Order
from .serializers import OrderSerializer
from drf_spectacular.utils import extend_schema


@extend_schema(tags=["Заказы"])
class OrderListApiView(generics.ListAPIView, generics.CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


order_list = OrderListApiView.as_view()
