from django.shortcuts import render
from .models import order as Order, OrderItem
from .serializers import *
from Product.models import Product
from django.contrib.auth.models import User
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
import uuid
import requests
from django.conf import settings


# Create your views here.

class OrderViewSet(ModelViewSet):
    queryset = order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        user = request.user
        products = request.data.get('products')
        amount = 0
        for product in products:
            product_id = product.get('product')
            quantity = product.get('quantity')
            amount += Product.objects.get(pk=product_id).price * quantity
        new_order = order.objects.create(user=user, amount=amount, status='PENDING', transaction_id=uuid.uuid4())
        for product in products:
            product_id = product.get('product')
            quantity = product.get('quantity')
            orderitem = OrderItem.objects.create(product=Product.objects.get(pk=product_id), quantity=quantity)
            orderitem.save()
            new_order.products.add(orderitem)
        serliazer = OrderSerializer(new_order)
        return Response(serliazer.data, status=201)
    


class SSLCommerzGateWayAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        store_id = settings.SSLCOMMERZ_STORE_ID
        store_passwd = settings.SSLCOMMERZ_STORE_PASSWORD
        url = settings.SSLCOMMERZ_CHECKOUT_URL
        order_id = request.data.get('order_id')
        order = Order.objects.get(pk=order_id)
        cus_email = request.user.email
        amount = order.amount
        currency = 'BDT'
        tran_id = order.transaction_id
        success_url = 'http://13.213.44.206:8000/payment/success/'
        fail_url = 'http://13.213.44.206:8000/payment/fail/'
        cancel_url = 'http://13.213.44.206:8000/payment/cancel/'
        product_category = 'None'
        cus_add1 = ''
        cus_city = 'Dhaka'
        cus_country = 'Bangladesh'
        cus_phone = '01XXXYYYZZZ'
        shipping_method = 'NO'
        product_name = 'Product Name',
        product_profile = 'None',

        post_data = {
            'store_id': store_id,
            'store_passwd': store_passwd,
            'total_amount': amount,
            'currency': currency,
            'tran_id': tran_id,
            'success_url': success_url,
            'fail_url': fail_url,
            'cancel_url': cancel_url,
            'product_category': product_category,
            'cus_email': cus_email,
            'cus_add1': cus_add1,
            'cus_city': cus_city,
            'cus_country': cus_country,
            'cus_phone': cus_phone,
            'shipping_method': shipping_method,
            'product_name': product_name,
            'product_profile': product_profile
        }

        response = requests.post(url, data=post_data, files=[])
        return Response(response.json(), status=response.status_code)
    


class SSLCommerzSuccessView(APIView):

    def post(self, request):
        data = request.data
        print(data)
        val_id = data.get('val_id')
        store_id = settings.SSLCOMMERZ_STORE_ID
        store_passwd = settings.SSLCOMMERZ_STORE_PASSWORD
        url = settings.SSLCOMMERZ_VALIDATE_URL
        post_data = {
            'store_id': store_id,
            'store_passwd': store_passwd,
            'val_id': val_id,
            'format': 'json'
        }
        response = requests.post(url, data=post_data, files=[])
        return Response(response.json(), status=response.status_code)


class SSLCommerzFailView(APIView):
    
        def post(self, request):
            data = request.data
            print(data)
            return Response(data=data, status=200)


class SSLCommerzCancelView(APIView):
    
        def post(self, request):
            data = request.data
            print(data)
            return Response(data=data, status=200)