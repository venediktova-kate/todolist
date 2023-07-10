from django.contrib.auth import login, logout
from rest_framework.response import Response
from rest_framework import generics, permissions

from core.models import User
from core.serializers import SignUpSerializer, LoginSerializer, ProfileSerializer, UpdatePasswordSerializer


class SignUpView(generics.CreateAPIView):
    """
    View для регистрации пользователя в системе
    """
    serializer_class = SignUpSerializer


class LoginView(generics.CreateAPIView):
    """
    View для авторизации пользователя
    """
    serializer_class = LoginSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        login(request=self.request, user=serializer.save())

        return Response(serializer.data)


class ProfileView(generics.RetrieveUpdateDestroyAPIView):
    """
    View для получения, обновления данных пользователя и логаута
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ProfileSerializer

    def get_object(self):
        return self.request.user

    def perform_destroy(self, instance: User):
        logout(self.request)


class UpdatePasswordView(generics.UpdateAPIView):
    """View для смены пароля"""
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UpdatePasswordSerializer

    def get_object(self):
        return self.request.user
