from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class MessengerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'instagram.messenger'
    verbose_name: str = _('Messenger')