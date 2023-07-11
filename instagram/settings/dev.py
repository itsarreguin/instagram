# Instagram development settings module

from instagram.settings.common import *


SECRET_KEY = 'django-insecure-&4s1p8-rj903ne#vv(h_hig_#$w+v!l%i2o@)&2xjru=le=#zs'

ALLOWED_HOSTS = []

DEBUG = True

INSTALLED_APPS += [
    'django_extensions',
    'debug_toolbar',
]

MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']

INTERNAL_IPS += ['127.0.0.1']


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


TEMPLATES[0]['OPTIONS']['context_processors'] += ['django.template.context_processors.debug']


MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

MEDIA_URL = 'media/'


# Celery settings
CELERY_TASK_ALWAYS_EAGER = True
CELERY_TASK_EAGER_PROPAGATES = True


# Email configuration
# https://docs.djangoproject.com/en/4.1/topics/email/#email-backends

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_HOST = 'smtp.mailtrap.io'
EMAIL_PORT = 2525
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER_DEV')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD_DEV')


# Django Debug Toolbar settings
# https://django-debug-toolbar.readthedocs.io/en/latest/configuration.html#debug-toolbar-panels

DEBUG_TOOLBAR_PANELS = [
    'debug_toolbar.panels.history.HistoryPanel',
    'debug_toolbar.panels.versions.VersionsPanel',
    'debug_toolbar.panels.timer.TimerPanel',
    'debug_toolbar.panels.settings.SettingsPanel',
    'debug_toolbar.panels.headers.HeadersPanel',
    'debug_toolbar.panels.request.RequestPanel',
    'debug_toolbar.panels.sql.SQLPanel',
    'debug_toolbar.panels.staticfiles.StaticFilesPanel',
    'debug_toolbar.panels.templates.TemplatesPanel',
    'debug_toolbar.panels.cache.CachePanel',
    'debug_toolbar.panels.signals.SignalsPanel',
    'debug_toolbar.panels.redirects.RedirectsPanel',
    'debug_toolbar.panels.profiling.ProfilingPanel',
]