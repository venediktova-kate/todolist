from rest_framework import generics
from core.serializers import SignUpSerializer


class SignUpView(generics.CreateAPIView):
    """
    View для регистрации пользователя в системе
    """
    serializer_class = SignUpSerializer
