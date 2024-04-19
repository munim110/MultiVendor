from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register('orders', OrderViewSet, basename='order')

urlpatterns = [
    path('payment/', SSLCommerzGateWayAPI.as_view(), name='payment')
] + router.urls