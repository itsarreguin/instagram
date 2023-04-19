from typing import Dict
from instagram.posts.forms import PostCreateForm


def post_form(request) -> Dict[str, PostCreateForm]:
    return { 'post_form': PostCreateForm }