from django.shortcuts import render

# Create your views here.

def addProduct(request):
    return render(request, 'product/add_product.html')