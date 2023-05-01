""" Account application config module """

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class AccountConfig(AppConfig):
    """ Account app config class """
    
    default_auto_field: str = 'django.db.models.BigAutoField'
    name: str = 'instagram.account'
    vaerbose_name: str = _('Account')
    
    def ready(self) -> None:
        from instagram.account import signals as signals
        return super().ready()