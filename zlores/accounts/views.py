from django.shortcuts import render
from django.contrib.auth import authenticate, login
# Create your views here.
def register_request(request):
    return render(request, 'register.html')

def login_request(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request,username=username,password=password)

        if user is not None:
            login(request,user)
            return render(request, 'index.html')
        
    return render(request, 'login.html')