from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import HttpResponse

# Create your views here.

def signin(request):
    return render(request, 'auth/login.html')


def register(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm-password')

        if password != confirm_password:
            return HttpResponse('Passwords do not match')
        
        new_user = User.objects.create_user(username=username, email=email, password=password)

        if new_user is None:
            return HttpResponse('User not created')
        
        new_user.first_name = firstname
        new_user.last_name = lastname
        new_user.save()

        # next class will be about how to handle errors
        # and redirecting to view functions rather than rendering templates
        return HttpResponse('User created successfully')

    return render(request, 'auth/signup.html')