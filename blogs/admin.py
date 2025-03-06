from django.contrib import admin
from .models import Post, Like, Comment

# Register your models here.
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at', 'likes_count', 'comments_count')
    list_filter = ('author', 'created_at')
    search_fields = ('title', 'content', 'author__username')
    ordering = ('-created_at',)
    # Opcional: Si deseas que los contadores se muestren como campos de solo lectura
    readonly_fields = ('likes_count', 'comments_count')

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'created_at')
    list_filter = ('user', 'post')
    search_fields = ('user__username', 'post__title')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'user', 'created_at', 'content')
    list_filter = ('post', 'user', 'created_at')
    search_fields = ('user__username', 'post__title', 'content')
    ordering = ('-created_at',)