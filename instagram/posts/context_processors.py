# Python stantard library
from typing import Dict

# Django imports
from django.http import HttpRequest
from django.forms import BaseForm

# Instagram models
from instagram.posts.models import Collection
# Instagram forms
from instagram.posts.forms import PostCreateForm


def post_form(request: HttpRequest) -> Dict[str, BaseForm] | None:
    if request.user.is_authenticated:
        return { 'post_form': PostCreateForm }
    return {}


def collections(request: HttpRequest) -> Dict[str, object] | None:
    user = request.user
    if request.user.is_authenticated:
        collections = Collection.objects.filter(user=user).all()
        return { 'collections': collections }
    
    return {}