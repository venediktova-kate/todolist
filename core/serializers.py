from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed
from django.core.exceptions import ValidationError
from rest_framework import serializers
from core.models import User
from core.fields import PasswordField


class SignUpSerializer(serializers.ModelSerializer):
    """
    Сериалайзер для регистрации пользователя
    """
    password = PasswordField(required=True)
    password_repeat = PasswordField(required=True)

    class Meta:
        model = User
        fields = ("id", "username", "first_name", "last_name", "email", "password", "password_repeat")

    def validate(self, attrs: dict) -> dict:
        """
        Проверка на совпадение введенных паролей
        """
        if attrs['password'] != attrs['password_repeat']:
            raise ValidationError({'password_repeat': 'Passwords must match'})
        return attrs

    def create(self, validated_data: dict) -> User:
        """
        Сохранение пользователя в БД
        """
        validated_data['password'] = make_password(validated_data['password'])
        user = User(
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
            password=validated_data['password'],
        )
        user.save()
        return user


class LoginSerializer(serializers.ModelSerializer):
    """    Сериалайзер для авторизации и аутентификации пользователя
    """
    username = serializers.CharField(required=True)
    password = PasswordField(required=True)

    class Meta:
        model = User
        fields = ("id", "username", "first_name", "last_name", "email", "password")
        read_only_fields = ("id", "first_name", "last_name", "email")

    def create(self, validated_data: dict) -> User:
        user = authenticate(
            username=validated_data['username'],
            password=validated_data['password']
        )
        if not user:
            raise AuthenticationFailed
        return user
