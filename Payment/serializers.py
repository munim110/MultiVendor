from rest_framework.serializers import ModelSerializer, PrimaryKeyRelatedField
from .models import *

class OrderSerializer(ModelSerializer):
    user = PrimaryKeyRelatedField(queryset=User.objects.all())
    class Meta:
        model = order
        fields = '__all__'
        depth = 1