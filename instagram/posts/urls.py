# Python standard library
from typing import List

# Django imports
from django.urls import path

# Instagram views
from instagram.posts.views import PostCreateView


app_name: str = 'posts'

urlpatterns: List[path] = [
    
    path(
        route = 'posts/new/',
        view = PostCreateView.as_view(),
        name = 'new'
    ),
]