""" Posts application config module """

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class PostsConfig(AppConfig):
    """ Posts app config class """
    
    default_auto_field: str = 'django.db.models.BigAutoField'
    name: str = 'instagram.posts'
    verbose_name: str = _('Posts')
    
    def ready(self) -> None:
        from instagram.posts import signals as signals
        return super().ready()