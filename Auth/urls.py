from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register('users', UserViewSet, basename='vendor')

urlpatterns = [
    path('login/', signin, name='login'),
    path('register/', register, name='register'),
    path('token/', ObtainTokenView.as_view(), name='token'),
    path('token/refresh/', AccessTokenFromRefreshToken.as_view(), name='refresh_token'),
] + router.urls