# Django database
from django.db import models
# Django config
from django.conf import settings
# Django utils
from django.utils.translation import gettext_lazy as _

# Instagram models
from instagram.core.models import BaseAbstractModel
from instagram.posts.models import Post


class Collection(BaseAbstractModel):
    
    name = models.CharField(_('name'), max_length=200, blank=False, null=False, default='default')
    slug = models.SlugField(_('slug'), max_length=200, blank=False, null=False, default='default')
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='collections'
    )
    posts = models.ManyToManyField(Post, related_name='posts')
    
    class Meta:
        verbose_name: str = _('Collection')
        verbose_name_plural: str = _('Collections')
    
    def __str__(self) -> str:
        return '%s' % self.name