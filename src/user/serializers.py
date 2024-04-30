from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    city = serializers.CharField(default=None)
    address = serializers.CharField(default=None)
    phone = serializers.CharField(default=None)
    is_staff = serializers.BooleanField(read_only=True)
    username = serializers.CharField(default="username", max_length=15)
    password = serializers.CharField(min_length=8, default="12345678", write_only=True)

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'password',
            'city',
            'address',
            'phone',
            'is_staff',

        )


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
