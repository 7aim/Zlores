from django.shortcuts import render
from post.models import Post

# Create your views here.
def home(request):
    posts = Post.objects.filter(is_active=True, is_home=True).order_by('-created_at')
    return render(request, 'home.html',{'posts': posts}) 