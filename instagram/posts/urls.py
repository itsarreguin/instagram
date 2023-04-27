# Python standard library
from typing import List

# Django imports
from django.urls import path

# Instagram views
from instagram.posts.views import PostCreateView
from instagram.posts.views import PostDetailView
from instagram.posts.views import LikeView
from instagram.posts.views import CommentCreateView
from instagram.posts.views import NewCollectionView


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
        route = 'collections/new/',
        view = NewCollectionView.as_view(),
        name = 'new-collection'
    ),
    path(
        route = 'p/<str:url>/like/',
        view = LikeView.as_view(),
        name = 'like'
    ),
    path(
        route = 'p/<slug:url>/comments/',
        view = CommentCreateView.as_view(),
        name = 'comment'
    ),
]