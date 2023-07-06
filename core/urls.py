from django.urls import path
from core.views import SignUpView, LoginView


app_name = 'core'
urlpatterns = [
    path('signup', SignUpView.as_view(), name='signup'),
    path('login', LoginView.as_view(), name='login'),
]
