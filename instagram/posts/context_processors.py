# Python stantard library
from typing import Dict
from typing import List

# Django HTTP package
from django.http import HttpRequest
# Django database
from django.db.models import Model
# Django forms
from django.forms import BaseForm

# Instagram models
from instagram.posts.models import Collection
from instagram.posts.models import Post
from instagram.posts.models import Like
# Instagram forms
from instagram.posts.forms import PostCreateForm


def post_form(request: HttpRequest) -> Dict[str, BaseForm | None]:
    if request.user.is_authenticated:
        return { 'post_form': PostCreateForm }
    
    return { 'post_form': None }


def collections(request: HttpRequest) -> Dict[str, List[Model]]:
    user = request.user
    if request.user.is_authenticated:
        collections = Collection.objects.filter(user=user).all()
        return { 'collections': collections }
    
    return { 'collections': [] }


def post_liked(request: HttpRequest) -> Dict[str, Model | None]:
    if request.user.is_authenticated:
        post = (
            Post.objects
            .filter(url=request.resolver_match.kwargs.get('url')).first()
        )
        liked = Like.objects.filter(user=request.user, post=post).first()
        return { 'liked': liked }
    
    return { 'liked': None }