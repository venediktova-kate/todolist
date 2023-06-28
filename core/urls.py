from django.urls import path
from core.views import SignUpSerializer

app_name = 'core'
urlpatterns = [
    path('signup', SignUpSerializer.as_view(), name='signup'),
]
