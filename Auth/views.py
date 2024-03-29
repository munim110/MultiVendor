from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout

# Create your views here.


def signin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponse('User logged in successfully')
        if '@' in username:
            user = User.objects.filter(email=username).first()
            if user is not None:
                username = user.username
        if user is not None:
            login(request, user)
            return HttpResponse('User logged in successfully')
        return render(request, 'auth/login.html', {'error': 'Invalid credentials'})
    return render(request, 'auth/login.html')


def register(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm-password')

        if User.objects.filter(email=email).exists():
            return render(request, 'auth/signup.html', {'error': 'Email already exists'})
        
        if User.objects.filter(username=username).exists():
            return render(request, 'auth/signup.html', {'error': 'Username already exists'})

        if password != confirm_password:
            return render(request, 'auth/signup.html', {'error': 'Passwords do not match'})
        
        new_user = User.objects.create_user(username=username, email=email, password=password)

        if new_user is None:
            return render(request, 'auth/signup.html', {'error': 'Error creating user'})
        
        new_user.first_name = firstname
        new_user.last_name = lastname
        new_user.save()

        # next class will be about how to handle errors
        # and redirecting to view functions rather than rendering templates
        return HttpResponse('User created successfully')

    return render(request, 'auth/signup.html')