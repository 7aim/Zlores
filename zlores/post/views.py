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
    comments = Comment.objects.filter(post=post).order_by('-created_at')
    return render(request, 'postdetail.html', {'post': post, 'comments' : comments})



@login_required
def createpost_request(request):
    if request.method == 'POST':
        title = request.POST['title']
        content = request.POST['content']
        image = request.FILES.get('image')
        post = Post.objects.create(title=title, content=content, image=image, author=request.user)
        post.save()
        return redirect('myposts')

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

@login_required
def likepost(request, id):
    post = get_object_or_404(Post, id=id)
    if request.user in post.likes.all():
        post.likes.remove(request.user)  # Zaten beğenmişse kaldır
    else:
        post.likes.add(request.user)  # Beğeni ekle
        post.dislikes.remove(request.user)  # Beğenmediyse kaldır
    return redirect(request.META.get('HTTP_REFERER', '/'))  # Geldiği sayfaya yönlendir

@login_required
def dislikepost(request, id):
    post = get_object_or_404(Post, id=id)
    if request.user in post.dislikes.all():
        post.dislikes.remove(request.user)  # Zaten beğenmemişse kaldır
    else:
        post.dislikes.add(request.user)  # Beğenmeme ekle
        post.likes.remove(request.user)  # Beğendiyse kaldır
    return redirect(request.META.get('HTTP_REFERER', '/'))  # Geldiği sayfaya yönlendir