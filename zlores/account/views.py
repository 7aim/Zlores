from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import Profile, Follow
from post.models import Post
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

def resetpassword_request(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        new_password = request.POST['new_password']

        if User.objects.filter(username=username).exists():
            user = User.objects.get(username=username)
            if user.email == email:
                user.set_password(new_password)
                user.save()
                return redirect('/login')
        
    return render(request, 'resetpassword.html')

@login_required
def profile_request(request):
    # Profile nesnesini kontrol et ve oluştur
    profile, created = Profile.objects.get_or_create(user=request.user)
    followers_count = Follow.objects.filter(following=request.user).count()  # Takipçi sayısı
    following_count = Follow.objects.filter(follower=request.user).count()  # Takip edilen kişi sayısı

    if request.method == "POST":
        form_type = request.POST.get('form_type')  # Hangi formun gönderildiğini kontrol et

        if form_type == "profile":
            # Profile formunu işle
            if request.POST.get('bio'):
                profile.bio = request.POST['bio']
            if request.POST.get('link'):
                profile.link = request.POST['link']
            if request.FILES.get('image'):
                profile.image = request.FILES['image']
            profile.save()
            return redirect('profile')

        elif form_type == "settings":
            # Settings formunu işle
            user = request.user
            if request.POST.get('username'):
                user.username = request.POST['username']
            if request.POST.get('first_name'):
                user.first_name = request.POST['first_name']
            if request.POST.get('last_name'):
                user.last_name = request.POST['last_name']
            if request.POST.get('email'):
                user.email = request.POST['email']

            # Kullanıcı adı veya e-posta zaten varsa kontrol et
            if User.objects.filter(username=user.username).exclude(id=user.id).exists() or User.objects.filter(email=user.email).exclude(id=user.id).exists():
                return redirect('profile')
            else:
                user.save()
                return redirect('profile')

    return render(request, 'profile.html', {
        'profile': profile,
        'followers_count': followers_count,
        'following_count': following_count,
    })

@login_required
def userprofile_request(request, author):
    user = get_object_or_404(User, username=author)
    profile = get_object_or_404(Profile, user=user)
    followers_count = Follow.objects.filter(following=user).count()  # Takipçi sayısı
    following_count = Follow.objects.filter(follower=user).count()  # Takip edilen kişi sayısı
    is_following = Follow.objects.filter(follower=request.user, following=user).exists()  # Takip durumu

    return render(request, 'userprofile.html', {
        'author': user,
        'profile': profile,
        'followers_count': followers_count,
        'following_count': following_count,
        'is_following': is_following,
    })

@login_required
def follow_request(request, author):
    user_to_follow = get_object_or_404(User, username=author)  # Takip edilecek kullanıcıyı al
    Follow.objects.get_or_create(follower=request.user, following=user_to_follow)  # Takip et
    return redirect('userprofile', author=author)  # Profil sayfasına yönlendir

@login_required
def unfollow_request(request, author):
    user_to_unfollow = get_object_or_404(User, username=author)  # Takipten çıkılacak kullanıcıyı al
    Follow.objects.filter(follower=request.user, following=user_to_unfollow).delete()  # Takipten çık
    return redirect('userprofile', author=author)  # Profil sayfasına yönlendir