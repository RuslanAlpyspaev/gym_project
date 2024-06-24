from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from users.views import UserViewSet
from environments.views import EnvironmentViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'environments', EnvironmentViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/', include('users.urls')),
    path('api/', include('environments.urls')),
]
