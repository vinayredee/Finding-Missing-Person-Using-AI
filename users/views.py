from django.shortcuts import render, redirect
from django.contrib import messages
import requests
from rest_framework.decorators import api_view
from django.contrib import messages
from .serializers import *


@api_view(['GET', 'POST'])
def signup(request):
    if request.method == 'POST':
        data = {
            "username": request.POST.get("username"),
            "email": request.POST.get("email"),
            "pass1": request.POST.get("pass1"),
            "pass2": request.POST.get("pass2"),
            "phone_number": request.POST.get("phone_number"),
            "address": request.POST.get("address")

        }
        
        # Check if both passwords match
        if data['pass1'] != data['pass2']:
            messages.error(request, 'Both Passwords are not the same')
            return redirect('signup')

        # Check if username already exists
        if User.objects.filter(username=data['username']).exists():
            messages.error(request, 'Username already exists. Please choose a different username.')
            return redirect('signup')

        # Serialize the data and save if valid
        sz = UserSerializer(data=data)
        if sz.is_valid():
            sz.save()  # Save new user to the database
            messages.success(request, "You have signed up successfully!")
            return redirect('signin')
        else:
            messages.error(request, "There was an error with your signup. Please check the form.")
    
    return render(request, 'users/signup.html')


@api_view(['GET', 'POST'])
def signin(request):
    uname = ''
    if request.method == 'POST':
        data = {
            "username": request.POST.get("username"),
            "password": request.POST.get("password"),
        }
        uname = data['username']
        try:
            user = User.objects.get(username=data['username'], pass1=data['password'])
            request.session['username'] = user.username
            messages.success(request, "Logged Successfully")
            return redirect('index')
        except User.DoesNotExist:
            messages.error(request, "Invalid Credentials")
            return redirect('signin')
    context = {'username': uname}
    return render(request, 'users/signin.html', context)


@api_view(['GET', 'POST'])
def signout(request):
    if 'username' in request.session:
        del request.session['username']
        messages.info(request, 'Logged out Successfully')
    return redirect('index')


def index(request):
    return render(request, 'users/index.html') 