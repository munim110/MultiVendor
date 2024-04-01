from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register('users', UserViewSet, basename='vendor')

urlpatterns = [
    path('login/', signin, name='login'),
    path('register/', register, name='register'),
] + router.urls