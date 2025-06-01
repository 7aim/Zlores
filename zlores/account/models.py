from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  
    bio = models.CharField(max_length=255) 
    link = models.URLField(max_length=255, blank=True, null=True) 
    image = models.ImageField(upload_to='profile/', blank=True, null=True, default='profile/default.jpg') 
    created_at = models.DateTimeField(auto_now_add=True) 
    updated_at = models.DateTimeField(auto_now=True) 

    def __str__(self):
        return f"{self.user.username}'s Profile"
    

class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following') 
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')  
    created_at = models.DateTimeField(auto_now_add=True)  # Takip etme tarixi

    def __str__(self):
        return f"{self.follower.username} follows {self.following.username}"

    class Meta:
        unique_together = ('follower', 'following')  # Eyni useri birden cox defe takip etmeyi engelle