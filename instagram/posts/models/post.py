# Django imports
from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

# Instagram models
from instagram.core.models import BaseAbstractModel


class Post(BaseAbstractModel):
    """ Post model """
    
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='posts'
    )
    image = models.ImageField(_('image'), blank=False, null=False, upload_to='posts/')
    description = models.TextField(_('description'), blank=True, null=True)
    url = models.SlugField(_('url'), unique=True, null=False)
    
    class Meta:
        verbose_name: str = _('Post')
        verbose_name_plural: str = _('Posts')
    
    def __str__(self) -> str:
        return 'Post by @%s' % self.author.username