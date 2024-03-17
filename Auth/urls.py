from django.urls import path
from .views import *

urlpatterns = [
    path('login/', signin, name='login'),
    path('register/', register, name='register'),
]