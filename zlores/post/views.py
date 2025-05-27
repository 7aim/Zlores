from django.shortcuts import render, redirect, get_object_or_404
from .models import Post
from django.contrib.auth.decorators import login_required

@login_required
def createpost_request(request):
    if request.method == 'POST':
        title = request.POST['title']
        content = request.POST['content']
        post = Post.objects.create(title=title, content=content,author=request.user)
        post.save()
        return redirect('/')

    return render(request, 'createpost.html') 

@login_required
def myposts_request(request):
    posts = Post.objects.filter(author=request.user, is_active=True).order_by('-created_at')
    return render(request, 'myposts.html', {'posts': posts})

@login_required
def post_detail_request(request, id):
    post = get_object_or_404(Post, id=id)
    return render(request, 'post_detail.html', {'post': post})