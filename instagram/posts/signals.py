# Python standard library
from typing import Any

# Django dispatch
from django.dispatch import receiver
# Django database
from django.db.models.signals import post_save
# Django utils
from django.utils.crypto import get_random_string
from django.utils.text import slugify

# Instagram models
from instagram.posts.models import Post
from instagram.posts.models import Comment
from instagram.posts.models import Collection
# Instagram utils
from instagram.core.utils.text import RAND_CHARS


@receiver(post_save, sender=Post)
def save_post_url(instance: Post, **kwargs: Any) -> None:
    """generate_url
    Signal that generates a random string to be saved as url for a post.

    Args:
        sender (Model): The model that sends the signal
        instance (Post model): Instance of the same model that send a signal
    """
    if not instance.url:
        instance.url = get_random_string(length=32, allowed_chars=RAND_CHARS)
        instance.save()


@receiver(post_save, sender=Comment)
def comment_url(instance: Comment, **kwargs: Any) -> None:
    """ Save a url for Comment model """
    if not instance.url:
        instance.url = get_random_string(length=16, allowed_chars=RAND_CHARS)
        instance.save()


@receiver(post_save, sender=Collection)
def collection_slug(instance: Collection, **kwargs: Any) -> None:
    """ Save collection name as slug """
    if not instance.slug:
        instance.slug = slugify(instance.name)
        instance.save()