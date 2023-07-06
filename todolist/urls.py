from django.contrib import admin
from django.urls import path, include
from core.views import SignUpView, LoginView, ProfileView


app_name = 'core'

core_patterns = ([
                     path('signup', SignUpView.as_view(), name='signup'),
                     path('login', LoginView.as_view(), name='login'),
                     path('profile', ProfileView.as_view(), name='profile'),
], 'core')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('core/', include(core_patterns)),
]
