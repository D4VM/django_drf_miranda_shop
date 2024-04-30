from rest_framework import generics, permissions, status, exceptions
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate, login, logout
from drf_spectacular.utils import extend_schema

from .serializers import UserSerializer, LoginSerializer
from .models import User


@extend_schema(tags=['User'])
class UserList(generics.ListAPIView):
    """
    Предоставляет API для получения списка пользователей.

    Возвращает список всех пользователей.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]


@extend_schema(tags=['User'])
class UserDetail(generics.RetrieveAPIView):
    """
    Предоставляет API для получения информации о конкретном пользователе.

    Позволяет получать информацию о конкретном пользователе по его идентификатору.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]


@extend_schema(tags=['User'])
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


@extend_schema(tags=['User'])
class UserCreate(generics.CreateAPIView):
    """
    Предоставляет API для создания нового пользователя.

    Позволяет создавать новых пользователей с уникальными именами.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        """
        Создает нового пользователя.

        Создает нового пользователя с уникальным именем и сохраняет его в базе данных.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data['username']
        password = serializer.validated_data['password']

        if User.objects.filter(username=username).exists():
            raise exceptions.AuthenticationFailed(detail="Username already exists.", code=status.HTTP_400_BAD_REQUEST)

        user = serializer.save()
        user.set_password(password)
        user.save()

        return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)


@extend_schema(tags=['User'])
class LoginView(APIView):
    """
    Предоставляет API для входа пользователя.

    Позволяет пользователям войти в систему с использованием своих учетных данных.
    """
    serializer_class = LoginSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        """
        Вход пользователя.

        Проверяет учетные данные пользователя и выполняет вход.
        """
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return Response({'message': 'Login successful'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


@extend_schema(tags=['User'])
class LogoutView(APIView):
    """
    Предоставляет API для выхода пользователя.

    Позволяет пользователям выйти из системы.
    """
    serializer_class = None
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        """
        Выход пользователя.

        Выполняет выход пользователя из системы.
        """
        logout(request)
        return Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)


