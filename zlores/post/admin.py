from django.contrib import admin
from .models import Post, Comment

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at', 'score', 'is_active')  # Görünen sütunlar
    list_filter = ('is_active', 'created_at')  # Filtreleme seçenekleri
    search_fields = ('title', 'content')  # Arama yapılacak alanlar

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'author', 'content', 'created_at')  # Görünen sütunlar