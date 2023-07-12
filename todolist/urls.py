from django.contrib import admin
from django.urls import path, include
from core.views import SignUpView, LoginView, ProfileView, UpdatePasswordView


app_name = 'core'

core_patterns = ([
                     path('signup', SignUpView.as_view(), name='signup'),
                     path('login', LoginView.as_view(), name='login'),
                     path('profile', ProfileView.as_view(), name='profile'),
                     path('update_password', UpdatePasswordView.as_view(), name='update_password')
], 'core')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('core/', include(core_patterns)),
    path('oauth/', include("social_django.urls", namespace="social")),
    path("goals/", include("goals.urls")),
]
