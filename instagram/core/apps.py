""" Core application config module """

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class CoreConfig(AppConfig):
    """ Core app config class """
    
    default_auto_field: str = 'django.db.models.BigAutoField'
    name: str = 'instagram.core'
    verbose_name: str = _('Core')