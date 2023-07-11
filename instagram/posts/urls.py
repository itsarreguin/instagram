# Python standard library
from typing import List

# Django imports
from django.urls import path

# Instagram posts views
from instagram.posts.views.posts import PostCreateView
from instagram.posts.views.posts import PostDetailView
from instagram.posts.views.posts import PostDeleteView
from instagram.posts.views.posts import LikeView
from instagram.posts.views.posts import CommentFeedView
from instagram.posts.views.posts import CommentCreateView
# Instagram bookmark views
from instagram.posts.views.bookmarks import NewCollectionView
from instagram.posts.views.bookmarks import CollectionsView
from instagram.posts.views.bookmarks import CollectionDetailView
from instagram.posts.views.bookmarks import SaveToCollectionView


app_name: str = 'posts'

urlpatterns: List[path] = [
    path('posts/new/', PostCreateView.as_view(), name='new'),
    path('p/<str:url>/', PostDetailView.as_view(), name='detail'),
    path('p/<str:url>/delete/', PostDeleteView.as_view(), name='delete'),
    path(
        route='p/<str:url>/like/',
        view=LikeView.as_view(),
        name='like'
    ),
    path(
        route='p/<slug:url>/comments/feed/',
        view=CommentFeedView.as_view(),
        name='comment-feed'
    ),
    path(
        route='p/<slug:url>/comments/',
        view=CommentCreateView.as_view(),
        name='comment'
    ),
    path(
        route='collections/new/',
        view=NewCollectionView.as_view(),
        name='new-collection'
    ),
    path(
        route='@<str:username>/bookmarks/',
        view=CollectionsView.as_view(),
        name='bookmarks'
    ),
    path(
        route='@<str:username>/bookmarks/<slug:slug>/',
        view=CollectionDetailView.as_view(),
        name='bookmark'
    ),
    path(
        route='<str:username>/collections/<slug:coll_slug>/p/<str:post_url>/save/',
        view=SaveToCollectionView.as_view(),
        name='save'
    )
]