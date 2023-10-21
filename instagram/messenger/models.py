import uuid

from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

from instagram.core.models import BaseAbstractModel


class Inbox(BaseAbstractModel):

    uuid = models.UUIDField(_('uuid'), unique=True, default=uuid.uuid4, editable=False)
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='inboxes', max_length=2)

    class Meta:
        verbose_name: str = _('Inbox')
        verbose_name_plural: str = _('Inboxes')
        ordering: list[str] = ['-modified']

    def __str__(self) -> str:
        return '%s' % str(self.uuid)


class Message(BaseAbstractModel):

    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='messages_sender'
    )
    receiver = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='messages'
    )
    body = models.TextField(_('body'))
    inbox = models.ForeignKey(Inbox, on_delete=models.CASCADE, related_name='messages')
    seen = models.BooleanField(_('seen'), default=False)

    class Meta:
        verbose_name: str = _('Message')
        verbose_name_plural: str = _('Messages')
        ordering: list[str] = ['created']

    def __str__(self) -> str:
        return 'from %s' % self.sender.username