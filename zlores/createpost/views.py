from django.shortcuts import render

def createpost_request(request):
    return render(request, 'createpost.html') 