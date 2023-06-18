from rest_framework import serializers

from .models import *  ## 정해진 모델만 import하게 설정해두었으므로 *로 import해도 문제 없음

__all__ = (
    "SignUpSerializer",
    "SignInSchema",
    "SignInSerializer",
    "UserSerializer",
)


class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "password", "team")


class SignInSchema(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "password")


class SignInSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "last_login")


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "team")


# class SignInSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
