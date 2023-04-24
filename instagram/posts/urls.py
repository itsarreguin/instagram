# Python standard library
from typing import List

# Django imports
from django.urls import path

# Instagram views
from instagram.posts.views import PostCreateView
from instagram.posts.views import PostDetailView
from instagram.posts.views import LikeView


app_name: str = 'posts'

urlpatterns: List[path] = [
    path(
        route = 'posts/new/',
        view = PostCreateView.as_view(),
        name = 'new'
    ),
    path(
        route = 'p/<str:url>/',
        view = PostDetailView.as_view(),
        name = 'detail'
    ),
    path(
        route = 'posts/<str:url>/like/',
        view = LikeView.as_view(),
        name = 'like'
    )
]