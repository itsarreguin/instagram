# Django imports
from django.db import models
from django.utils.translation import gettext_lazy as _

# Instagram imports
from instagram.core.models import BaseAbstractModel
from instagram.account.models import User


class Profile(BaseAbstractModel):
    
    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE,)
    picture = models.ImageField(_('profile picture'), blank=True, null=True, upload_to='users/')
    biography = models.CharField(_('biography'), max_length=325, blank=True, null=True)
    link = models.URLField(_('link'), max_length=255, blank=True, null=True)
    is_public = models.BooleanField(_('is public'), default=True)
    
    class Meta:
        verbose_name: str = _('Profile')
        verbose_name_plural: str = _('Profiles')
    
    def __str__(self) -> str:
        return '%s' % self.user.username