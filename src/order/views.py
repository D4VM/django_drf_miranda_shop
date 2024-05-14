from rest_framework import generics
from drf_spectacular.utils import extend_schema
from .models import Order
from .serializers import OrderSerializer
from .permisions import OrderPermissions

from .invoice import InvoiceSerializer

# TODO: Invoice Generation


@extend_schema(tags=["Заказы"])
class OrderListApiView(
    generics.ListAPIView,
    generics.CreateAPIView,
):

    # queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [OrderPermissions]

    def get_queryset(self):
        """
        This view should return a list of all the purchases
        for the currently authenticated user.
        """

        user = self.request.user
        if not user.is_staff:
            return Order.objects.filter(user=user)
        return Order.objects.all()


order_list = OrderListApiView.as_view()


@extend_schema(tags=["Заказы"])
class OrderDetailAPIView(generics.RetrieveAPIView):
    serializer_class = OrderSerializer
    permission_classes = [OrderPermissions]
    lookup_field = "pk"

    def get_queryset(self):
        """
        This view should return the order detail.
        """
        user = self.request.user
        order_id = self.kwargs.get("pk")  # Retrieve order id from URL kwargs
        if not user.is_staff:
            return Order.objects.filter(pk=order_id, user=user)
        return Order.objects.all()


order_detail = OrderDetailAPIView.as_view()
