# Django imports
from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

# Instagram models
from instagram.core.models import BaseAbstractModel
from instagram.posts.models import Post


class Comment(BaseAbstractModel):
    """ Comment model """
    
    author = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='comments'
    )
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    body = models.TextField(_('body'), blank=True, null=False)
    url = models.SlugField(_('url'), max_length=180, unique=True, null=False)
    
    class Meta:
        verbose_name: str = _('Comment')
        verbose_name_plural: str = _('Comments')
    
    def __str__(self) -> str:
        return 'Comment by @%s' % self.author.username


class Like(BaseAbstractModel):
    """ Like model """
    
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='likes'
    )
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    
    class Meta:
        verbose_name: str = _('Like')
        verbose_name_plural: str = _('Likes')
    
    def __str__(self) -> str:
        return 'Like by @%s' % self.user.username