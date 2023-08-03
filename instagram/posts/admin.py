# Python standard library
from typing import List

# Django imports
from django.contrib import admin

# Instagram models
from instagram.posts.models import Post
from instagram.posts.models import Comment
from instagram.posts.models import Like
from instagram.posts.models import Collection


@admin.register(Post)
class PostModelAdmin(admin.ModelAdmin):

    list_display: List[str] = ['id', 'author', 'url']
    list_display_links: List[str] = ['author', 'url']


@admin.register(Comment)
class CommentModelAdmin(admin.ModelAdmin):

    list_display: List[str] = ['id', 'author', 'post']
    list_display: List[str] = ['author', 'post']


@admin.register(Like)
class LikeModelAdmin(admin.ModelAdmin):

    list_display: List[str] = ['id', 'user', 'post']
    list_display_links: List[str] = ['user', 'post']


@admin.register(Collection)
class CollectionModelAdmin(admin.ModelAdmin):
    pass