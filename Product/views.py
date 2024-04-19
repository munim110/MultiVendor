from django.shortcuts import render, redirect
from .models import *
from Vendor.models import Vendor
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter
from .serializers import *
from .permissions import *


# Create your views here.


@login_required(login_url='login')
def addProduct(request):
    if not Vendor.objects.filter(user=request.user).exists():
        return redirect('login')
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        stock = request.POST.get('stock')
        is_active = True if request.POST.get('is_active') == 'on' else False
        image = request.FILES.get('image')
        print(name, description, price, stock, is_active, image)
        try:
            product = Product.objects.create(
                name = name,
                description = description,
                price = price,
                stock = stock,
                is_active = is_active,
                image = image,
                vendor = Vendor.objects.get(user=request.user)
            )
            product.save()
            return render(request, 'product/add_product.html', {'message': 'Product added successfully'})
        except Exception as e:
            print(e)
            return render(request, 'product/add_product.html', {'message': 'Failed to add product'})

    return render(request, 'product/add_product.html')


def viewAllProducts(request):
    products = Product.objects.all()
    return render(request, 'product/view_all_products.html', {'products': products})


def viewProduct(request, id):
    try:
        product = Product.objects.get(pk=id)
        return render(request, 'product/product_details.html', {'product': product})
    except Product.DoesNotExist:
        return render(request, 'product/product_details.html', {'message': 'Product not found'})
    

@login_required(login_url='login')
def editProduct(request, id):
    try:
        product = Product.objects.get(pk=id)
        if product.vendor.user != request.user:
            return HttpResponse('You are not authorized to edit this product')
        if request.method == 'POST':
            product.name = request.POST.get('name')
            product.description = request.POST.get('description')
            product.price = request.POST.get('price')
            product.stock = request.POST.get('stock')
            product.is_active = True if request.POST.get('is_active') == 'on' else False
            product.image = request.FILES.get('image') if request.FILES.get('image') else product.image
            product.save()
            return render(request, 'product/edit_product.html', {'message': 'Product updated successfully'})
        return render(request, 'product/edit_product.html', {'product': product})
    except Product.DoesNotExist:
        return render(request, 'product/edit_product.html', {'message': 'Product not found'})
    

@api_view(['GET'])
def demoAPI(request):
    response = {
        "Name": "Product API",
        "Message": "This is a demo API for Product"
    }
    return Response(response, status=status.HTTP_200_OK)


# Information about API Requests

# GET -> To get data
# POST -> To create data
# PUT -> To update data
# DELETE -> To delete data
# PATCH -> To partially update data


# HTTP Status Codes

# 200 -> OK -> Successful Request
# 201 -> Created -> Successful Post Request
# 204 -> No Content -> Successful Delete Request
# 400 -> Bad Request -> Client Side Error
# 401 -> Unauthorized -> Authentication Error
# 403 -> Forbidden -> Authorization Error
# 404 -> Not Found -> Resource Not Found
# 405 -> Method Not Allowed -> Invalid Method
# 500 -> Internal Server Error -> Server Side Error
# 502 -> Bad Gateway -> Server Side Error
# 503 -> Service Unavailable -> Server Side Error
# 504 -> Gateway Timeout -> Server Side Error
# 505 -> HTTP Version Not Supported -> Server Side Error
# 507 -> Insufficient Storage -> Server Side Error
# 511 -> Network Authentication Required -> Server Side Error
# 520 -> Unknown Error -> Server Side Error

class demoAPIView(APIView):

    def get(self, request):
        if not request.user.is_authenticated:
            return Response({'error': 'You are not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)
        if not request.user.is_staff and not request.user.is_superuser:
            return Response({'error': 'You are not authorized to access this API'}, status=status.HTTP_403_FORBIDDEN)
        response = {
        "Name": "Product API",
        "Message": "This is a demo API for Product"
    }
        return Response(response, status=status.HTTP_200_OK)
    
    def post(self, request):
        return Response({'message': 'Post Request'}, status=status.HTTP_201_CREATED)
    
    def put(self, request):
        return Response({'message': 'Put Request'}, status=status.HTTP_200_OK)
    
    def delete(self, request):
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def patch(self, request):
        return Response({'message': 'Patch Request'}, status=status.HTTP_200_OK)
    

class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    # permission_classes = [IsAuthenticated]
    filter_backends = [SearchFilter]
    search_fields = ['name', 'description']


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [CustomPermission]


# write a ModelViewSet for Products
# Each vendor should be able to see only their products
# and the API cannot be accessed by an unauthenticated user and those who are not vendors

class ProductOfVendorViewset(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [CustomProductPermission]

    def get_queryset(self):
        return Product.objects.filter(vendor__user=self.request.user)