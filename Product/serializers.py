from rest_framework.serializers import ModelSerializer
from Product.models import Product, Category

class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
        extra_kwargs = {
            'vendor': {'read_only': True}
        
        }


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'