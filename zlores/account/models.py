from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Kullanıcı ile ilişki
    bio = models.CharField(max_length=255)  # Bio
    link = models.URLField(max_length=255, blank=True, null=True)  # Link
    image = models.ImageField(upload_to='profile/', blank=True, null=True, default='profile/default.jpg')  # Fotoğraf alanı
    created_at = models.DateTimeField(auto_now_add=True)  # Oluşturulma tarihi
    updated_at = models.DateTimeField(auto_now=True)  # Güncellenme tarihi

    def __str__(self):
        return f"{self.user.username}'s Profile"
    

class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')  # Takip eden kullanıcı
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')  # Takip edilen kullanıcı
    created_at = models.DateTimeField(auto_now_add=True)  # Takip etme tarihi

    def __str__(self):
        return f"{self.follower.username} follows {self.following.username}"

    class Meta:
        unique_together = ('follower', 'following')  # Aynı kullanıcıyı birden fazla kez takip etmeyi engelle