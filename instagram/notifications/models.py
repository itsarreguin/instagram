# Python standard library
from typing import Type
from datetime import datetime

# Django database
from django.db import models
# Django config
from django.conf import settings
# Django utils
from django.utils.translation import gettext_lazy as _


class NotificationType(models.TextChoices):

    FOLLOWER = 'follower', _('New follower')
    LIKE = 'like', _('New like')
    COMMENT = 'comment', _('New comment')
    MESSAGE = 'message', _('New Message')


class Notification(models.Model):

    receiver = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, related_name='notifications',
        on_delete=models.CASCADE
    )
    sender = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, related_name='sender',
        on_delete=models.CASCADE
    )
    category = models.CharField(
        _('category'), max_length=100, blank=False, null=False,
        choices=NotificationType.choices
    )
    object_id = models.IntegerField(_('object id'), blank=True, null=True)
    object_slug = models.CharField(
        _('object slug'), max_length=200, blank=True, null=True
    )
    slug = models.SlugField(_('slug'), max_length=100, unique=True)
    is_read = models.BooleanField(_('is read'), default=False)
    created = models.DateTimeField(_('created'), auto_now_add=True)

    class Meta:
        verbose_name: str = _('Notification')
        verbose_name_plural: str = _('Notifications')

    def __str__(self) -> str:
        return f'from {self.sender.username}'

    @property
    def formated_timestamp(self) -> Type[datetime]:
        return self.created.strftime('%d/%m/%Y-%H/%M/%S')