from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    city = serializers.CharField(default=None)
    address = serializers.CharField(default=None)
    phone = serializers.CharField(default=None)
    is_staff = serializers.BooleanField(read_only=True)
    username = serializers.CharField(default="username", max_length=15)
    password = serializers.CharField(min_length=8, default="12345678", write_only=True)
    email = serializers.EmailField(default="example@example.com")

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "password",
            "email",
            "city",
            "address",
            "phone",
            "is_staff",
        )

        read_only_fields = ("token",)


class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User(
            username=validated_data["username"],
        )
        user.set_password(validated_data["password"])
        user.save()
        return user
