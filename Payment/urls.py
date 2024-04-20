from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register('orders', OrderViewSet, basename='order')

urlpatterns = [
    path('payment/', SSLCommerzGateWayAPI.as_view(), name='payment'),
    path('success/', SSLCommerzSuccessView.as_view(), name='success'),
    path('fail/', SSLCommerzFailView.as_view(), name='fail'),
    path('cancel/', SSLCommerzCancelView.as_view(), name='cancel'),

] + router.urls