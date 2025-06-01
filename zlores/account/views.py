from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import Profile, Follow
from post.models import Post
from django.contrib.auth.decorators import login_required

# REGISTER
def register_request(request):
    if request.method == "POST":
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST.get('password')

        # Username uzunluq yoxlanisie
        if len(username) < 3:
            return render(request, 'register.html', {
                'errormessage': 'Username must be at least 3 characters long.'
            })
        
        # Password uzunluq yoxlanisi
        if len(password) < 5:
            return render(request, 'register.html', {
                'errormessage': 'Password must be at least 5 characters long.'
            })

        # Email ve usernamenin olub olmama yoxlanisi
        if User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists():
            return render(request, 'register.html', {
                'errormessage': 'Username or email already exists.'
            })
        
        user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name, email=email, password=password)
        user.save()
        return redirect('login')

    return render(request, 'register.html')

# LOGIN
def login_request(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        # User axtarisi
        user = authenticate(request,username=username,password=password)

        # Userin olub olmama yoxlanisi
        if user is not None:
            login(request,user)
            return redirect('/')
        else:
            return render(request, 'login.html', {
                'errormessage': 'Incorrect username or password.'
            })
        
    return render(request, 'login.html')

# RESET PASSWORD
def resetpassword_request(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        new_password = request.POST['new_password']

        # Yeni password uzunluq yoxlanisi
        if len(new_password) < 5:
            return render(request, 'resetpassword.html', {
                'errormessage': 'New password must be at least 5 characters long.'
            })

        # User varsa sifre deyisdir
        if User.objects.filter(username=username).exists():
            user = User.objects.get(username=username)
            if user.email == email:
                user.set_password(new_password)
                user.save()
                return redirect('/login')
            else:
                return render(request, 'login.html', {
                    'errormessage': 'User not found.'
                })
        else:
            return render(request, 'login.html', {
                'errormessage': 'User not found.'
            })
        
    return render(request, 'resetpassword.html')

# LOGOUT
@login_required
def logout_request(request):
    logout(request)
    return redirect('/')

# PROFILE
@login_required
def profile_request(request):
    # Profile modelini kontrol et ve yarat
    profile, created = Profile.objects.get_or_create(user=request.user)
    followers_count = Follow.objects.filter(following=request.user).count()
    following_count = Follow.objects.filter(follower=request.user).count()

    if request.method == "POST":
        form_type = request.POST.get('form_type')  # Hangi formun gönderildiğini belirle

        if form_type == "profile":
            # Profil bilgilerini güncelle
            if request.POST.get('bio'):
                profile.bio = request.POST['bio']
            if request.POST.get('link'):
                profile.link = request.POST['link']
            if request.FILES.get('image'):
                profile.image = request.FILES['image']
            profile.save()
            return redirect('profile')

        elif form_type == "settings":
            # Kullanıcı bilgilerini güncelle
            user = request.user

            # Kullanıcı adı uzunluk kontrolü
            new_username = request.POST.get('username')
            if new_username and len(new_username) < 3:
                return render(request, 'profile.html', {
                    'profile': profile,
                    'followers_count': followers_count,
                    'following_count': following_count,
                    'errormessage': 'Username must be at least 3 characters long.'
                })

            # Kullanıcı adı ve e-posta kontrolü
            if User.objects.filter(username=new_username).exclude(id=user.id).exists():
                return render(request, 'profile.html', {
                    'profile': profile,
                    'followers_count': followers_count,
                    'following_count': following_count,
                    'errormessage': 'Username already exists.'
                })

            if User.objects.filter(email=request.POST.get('email')).exclude(id=user.id).exists():
                return render(request, 'profile.html', {
                    'profile': profile,
                    'followers_count': followers_count,
                    'following_count': following_count,
                    'errormessage': 'Email already exists.'
                })

            # Kullanıcı bilgilerini güncelle
            if new_username:
                user.username = new_username
            if request.POST.get('first_name'):
                user.first_name = request.POST['first_name']
            if request.POST.get('last_name'):
                user.last_name = request.POST['last_name']
            if request.POST.get('email'):
                user.email = request.POST['email']

            user.save()
            return redirect('profile')

    return render(request, 'profile.html', {
        'profile': profile,
        'followers_count': followers_count,
        'following_count': following_count,
    })

# USER PROFILE
@login_required
def userprofile_request(request, author):
    user = get_object_or_404(User, username=author)
    profile = get_object_or_404(Profile, user=user)
    followers_count = Follow.objects.filter(following=user).count() 
    following_count = Follow.objects.filter(follower=user).count() 
    is_following = Follow.objects.filter(follower=request.user, following=user).exists()  # Takip durumu

    return render(request, 'userprofile.html', {
        'author': user,
        'profile': profile,
        'followers_count': followers_count,
        'following_count': following_count,
        'is_following': is_following,
    })

# FOLLOW
@login_required
def follow_request(request, author):
    user_to_follow = get_object_or_404(User, username=author)  # Takip edilecek useri al
    Follow.objects.get_or_create(follower=request.user, following=user_to_follow)  # Takip et
    return redirect('userprofile', author=author)  

# UNFOLLOW
@login_required
def unfollow_request(request, author):
    user_to_unfollow = get_object_or_404(User, username=author)  # Takipten cixarilacaq useri al
    Follow.objects.filter(follower=request.user, following=user_to_unfollow).delete()  # Takipten çık
    return redirect('userprofile', author=author)