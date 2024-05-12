from rest_framework import generics
from .models import Order, OrderItems
from .serializers import OrderSerializer


class OrderListApiView(generics.ListAPIView, generics.CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


order_list = OrderListApiView.as_view()