from django.db import models
from django.utils.translation import gettext_lazy as _


class BaseAbstractModel(models.Model):
    """ Instagram base abstract model class

    This is an abstract model for model inheritance
    """

    created = models.DateTimeField(_('created'), auto_now_add=True)
    modified = models.DateTimeField(_('modified'), auto_now=True)

    class Meta:
        abstract = True
        get_latest_by = 'modified'
        ordering = ['-created', '-modified']