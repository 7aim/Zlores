from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    title = models.CharField(max_length=255)  # Başlık
    content = models.TextField()  # İçerik
    image = models.ImageField(upload_to='postimages/', blank=True, null=True)  # Fotoğraf alanı
    author = models.ForeignKey(User, on_delete=models.CASCADE)  # Kullanıcı ile ilişki
    created_at = models.DateTimeField(auto_now_add=True)  # Oluşturulma tarihi
    updated_at = models.DateTimeField(auto_now=True)  # Güncellenme tarihi
    likes = models.ManyToManyField(User, related_name='likedposts', blank=True)  # Like alanı
    dislikes = models.ManyToManyField(User, related_name='dislikedposts', blank=True)  # Dislike alanı
    is_active = models.BooleanField(default=True)  # Post aktif mi?
    is_home = models.BooleanField(default=False)  # Post kesfet mi?
    

    def __str__(self):
        return self.title

    def totallikes(self):
        return self.likes.count()

    def totaldislikes(self):
        return self.dislikes.count()
    
class Comment(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='comments')  # Post ile ilişki
    author = models.ForeignKey(User, on_delete=models.CASCADE)  # Yorum yazarı
    content = models.TextField()  # Yorum içeriği
    created_at = models.DateTimeField(auto_now_add=True)  # Yorum oluşturulma tarihi

    def __str__(self):
        return f"Comment by {self.author} on {self.post}"