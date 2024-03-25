from django.shortcuts import render, redirect
from .models import Product
from Vendor.models import Vendor
from django.contrib.auth.decorators import login_required

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