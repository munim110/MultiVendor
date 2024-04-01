from rest_framework.serializers import ModelSerializer
from .models import *


class VendorSerializer(ModelSerializer):
    class Meta:
        model = Vendor
        fields = '__all__'