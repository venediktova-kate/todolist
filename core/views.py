from django.contrib.auth import login
from rest_framework.response import Response
from rest_framework import generics
from core.serializers import SignUpSerializer, LoginSerializer


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