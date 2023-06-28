from django.contrib import admin
from django.urls import path, include
from core.views import SignUpView


app_name = 'core'

core_patterns = ([
                     path('signup', SignUpView.as_view(), name='signup'),
], 'core')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('core/', include(core_patterns)),
]
