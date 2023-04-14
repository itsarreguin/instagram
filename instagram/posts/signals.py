# Python standard library
from typing import Any
from typing import Dict

# Django imports
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.db.models import Model
from django.utils.crypto import get_random_string

# Instagram models
from instagram.posts.models import Post
# Instagram utils
from instagram.core.utils import RAND_CHARS


@receiver(post_save, sender=Post)
def save_post_url(sender: Model, instance: Post, **kwargs: Dict[str, Any]) -> None:
    """generate_url
    Signal that generates a random string to be saved as url for a post.
    
    Args:
        sender (Model): The model that sends the signal
        instance (Post model): Instance of the same model that send a signal
    """
    if not instance.url:
        instance.url = get_random_string(length=64, allowed_chars=RAND_CHARS)
        instance.save()