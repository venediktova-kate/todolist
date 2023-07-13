from django.contrib import admin
from django.urls import path, include

from todolist import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('core/', include("core.urls")),
    path('oauth/', include("social_django.urls", namespace="social")),
    path("goals/", include("goals.urls")),
]

if settings.DEBUG:
    urlpatterns += [path('api-auth/', include('rest_framework.urls'))]
