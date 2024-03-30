from rest_framework.serializers import ModelSerializer
from Product.models import Product

class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'