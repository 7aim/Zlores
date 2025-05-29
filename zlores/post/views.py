from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Comment
from django.contrib.auth.decorators import login_required


@login_required
def myposts_request(request):
    posts = Post.objects.filter(author=request.user, is_active=True).order_by('-created_at')
    return render(request, 'myposts.html', {'posts': posts})

@login_required
def post_detail_request(request, id):
    post = get_object_or_404(Post, id=id)
    return render(request, 'postdetail.html', {'post': post})



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
def deletepost_request(request, id):
    post = get_object_or_404(Post, id=id, author=request.user)
    post.delete()
    return redirect('/')

@login_required
def updatepost_request(request, id):
    post = get_object_or_404(Post, id=id, author=request.user)
    if request.method == "POST":
        if request.POST['title']:
            post.title = request.POST['title']
        if request.POST['content']:
            post.content = request.POST['content']
        post.save()
        return redirect('postdetail', id=post.id)
    return render(request, 'updatepost.html', {'post': post})




@login_required
def addcomment_request(request, id):
    post = get_object_or_404(Post, id=id)
    if request.method == "POST":
        content = request.POST['commentcontent'] 
        if content:
            # Yeni bir yorum oluştur ve kaydet
            Comment.objects.create(post=post, author=request.user, content=content)
        return redirect('postdetail', id=post.id) 
    return redirect('postdetail', id=post.id)

@login_required
def deletecomment_request(request, postid, commentid):
    post = get_object_or_404(Post, id=postid)
    comment = get_object_or_404(Comment, post=post, id=commentid)
    comment.delete()
    return redirect('postdetail', id=post.id)