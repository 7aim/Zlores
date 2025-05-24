from django.shortcuts import render, redirect
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