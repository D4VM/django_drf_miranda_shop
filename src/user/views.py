from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from drf_spectacular.utils import extend_schema
from django.contrib.auth import authenticate

from .serializers import UserSerializer, LoginSerializer
from .models import User


@extend_schema(tags=["Пользователь"])
class UserList(generics.ListAPIView):
    """
    Предоставляет API для получения списка пользователей.

    Возвращает список всех пользователей.
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]


@extend_schema(tags=["Пользователь"])
class UserDetail(generics.RetrieveAPIView):
    """
    Предоставляет API для получения информации о конкретном пользователе.

    Позволяет получать информацию о конкретном пользователе по его идентификатору.
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]


@extend_schema(tags=["Пользователь"])
class UserME(generics.RetrieveAPIView):
    """
    Предоставляет API для получения информации о текущем пользователе.

    Позволяет получать информацию о текущем авторизованном пользователе.
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        """
        Получает информацию о текущем авторизованном пользователе.

        Возвращает данные авторизованного пользователя.
        """
        user = request.user
        instance = self.queryset.get(pk=user.pk)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


@extend_schema(
    tags=["Регистрация & Авторизация"], request=UserSerializer, responses=UserSerializer
)
@api_view(["POST"])
def register_user(request):
    if request.method == "POST":
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    tags=["Регистрация & Авторизация"], request=LoginSerializer, responses=None
)
@api_view(["POST"])
def user_login(request):
    if request.method == "POST":
        username = request.data.get("username")
        password = request.data.get("password")

        user = None

        if not user:
            user = authenticate(username=username, password=password)

        if user:
            token, _ = Token.objects.get_or_create(user=user)
            response = Response({"token": token.key}, status=status.HTTP_200_OK)
            response.set_cookie("token", token.key)
            return response


@extend_schema(tags=["Регистрация & Авторизация"], request=None, responses=None)
@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def user_logout(request):
    if request.method == "POST":
        try:
            # Delete the user's token to logout
            request.user.auth_token.delete()

            response = Response(
                {"message": "Successfully logged out."}, status=status.HTTP_200_OK
            )
            response.delete_cookie("token")
            return response
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
