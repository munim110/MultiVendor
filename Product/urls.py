from django.urls import path
from .views import *

urlpatterns = [
    path('add/', addProduct, name='add_product'),
]