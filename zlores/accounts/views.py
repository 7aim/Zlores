from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

def login_request(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request,username=username,password=password)

        if user is not None:
            login(request,user)
            return redirect('/')
        
    return render(request, 'login.html')

def register_request(request):
    if request.method == "POST":
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST.get('password')

        if User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists():
            return redirect('/')
        else:
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name, email=email, password=password)
            user.save()
            return redirect('login')

    return render(request, 'register.html')

def logout_request(request):
    logout(request)
    return redirect('/')

@login_required
def profile_request(request):
    if request.method == "POST":
        user = request.user

        if request.POST['username']:
            user.username = request.POST['username']
        if request.POST['first_name']:
            user.first_name = request.POST['first_name']
        if request.POST['last_name']:
            user.last_name = request.POST['last_name']
        if request.POST['email']:
            user.email = request.POST['email']

        if User.objects.filter(username=user.username).exclude(id=user.id).exists() or User.objects.filter(email=user.email).exclude(id=user.id).exists():
            return redirect('/')
        else:
            user.save()
            return redirect('/')
    
    return render(request, 'profile.html')