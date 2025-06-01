from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    title = models.CharField(max_length=255) 
    content = models.TextField()  
    image = models.ImageField(upload_to='postimages/', blank=True, null=True)  
    author = models.ForeignKey(User, on_delete=models.CASCADE)  
    created_at = models.DateTimeField(auto_now_add=True) 
    updated_at = models.DateTimeField(auto_now=True) 
    likes = models.ManyToManyField(User, related_name='likedposts', blank=True)  
    dislikes = models.ManyToManyField(User, related_name='dislikedposts', blank=True)  
    is_active = models.BooleanField(default=True) 
    is_home = models.BooleanField(default=False) 
    
    def __str__(self):
        return self.title

    def totallikes(self):
        return self.likes.count()

    def totaldislikes(self):
        return self.dislikes.count()
    
class Comment(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='comments') 
    author = models.ForeignKey(User, on_delete=models.CASCADE) 
    content = models.TextField() 
    created_at = models.DateTimeField(auto_now_add=True) 

    def __str__(self):
        return f"Comment by {self.author} on {self.post}"