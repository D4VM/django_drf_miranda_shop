from rest_framework import generics, status, exceptions, permissions
from drf_spectacular.utils import extend_schema

from .models import Order
from .serializers import OrderSerializer


@extend_schema(tags=['Order'])
class OrderListCreateAPIView(generics.ListCreateAPIView):
    """
    Возвращает набор данных заказов в зависимости от пользователя.

        Если пользователь не авторизован, возбуждает исключение PermissionDenied.
        Если пользователь не является администратором, возвращает заказы, связанные с этим пользователем.
        Если пользователь является администратором, возвращает все заказы.

    Создает заказ, связывая его с текущим пользователем.

        Если пользователь не авторизован, возбуждает исключение PermissionDenied.
    """

    serializer_class = OrderSerializer

    def get_queryset(self):

        user = self.request.user
        if user.is_anonymous:
            raise exceptions.PermissionDenied(code=status.HTTP_401_UNAUTHORIZED)
        if not user.is_staff:
            return Order.objects.filter(user=user)
        return Order.objects.all()

    def perform_create(self, serializer):
        user = self.request.user

        if user.is_anonymous:
            raise exceptions.PermissionDenied(code=status.HTTP_401_UNAUTHORIZED)

        return serializer.save(user=user)


@extend_schema(tags=['Order'])
class OrderUpdateAPIView(generics.UpdateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAdminUser]
    lookup_field = 'pk'


@extend_schema(tags=['Order'])
class OrderDestroyAPIView(generics.DestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAdminUser]
    lookup_field = 'pk'
