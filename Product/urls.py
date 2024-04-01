from django.urls import path
from .views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('products', ProductViewSet, basename='product')
router.register('categories', CategoryViewSet, basename='category')

urlpatterns = [
    path('add/', addProduct, name='add_product'),
    path('view/', viewAllProducts, name='view_all_products'),
    path('view/<int:id>/', viewProduct, name='view_product'),
    path('edit/<int:id>/', editProduct, name='edit_product'),
    path('demo/', demoAPIView.as_view(), name='demo'),
] + router.urls