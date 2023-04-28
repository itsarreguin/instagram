# Python standard library
from typing import List

# Django imports
from django.urls import path

# Instagram posts views
from instagram.posts.views.posts import PostCreateView
from instagram.posts.views.posts import PostDetailView
from instagram.posts.views.posts import LikeView
from instagram.posts.views.posts import CommentCreateView
# Instagram bookmark views
from instagram.posts.views.bookmarks import NewCollectionView
from instagram.posts.views.bookmarks import CollectionsView
from instagram.posts.views.bookmarks import CollectionDetailView


app_name: str = 'posts'

urlpatterns: List[path] = [
    path('posts/new/', PostCreateView.as_view(), name='new'),
    path(
        route = 'p/<str:url>/',
        view = PostDetailView.as_view(),
        name = 'detail'
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
    path(
        route = 'collections/new/',
        view = NewCollectionView.as_view(),
        name = 'new-collection'
    ),
    path(
        route = '@<str:username>/bookmarks/',
        view = CollectionsView.as_view(),
        name = 'bookmarks'
    ),
    path(
        route = '@<str:username>/bookmarks/<slug:slug>/',
        view = CollectionDetailView.as_view(),
        name = 'bookmark'
    ),
]