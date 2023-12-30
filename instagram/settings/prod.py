# Instagram production settings module

from instagram.settings.common import *


SECRET_KEY = os.environ.get('SECRET_KEY', None)

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS').split(',')

DEBUG = False

INTERNAL_IPS = os.environ.get('INTERNAL_IPS').split(',')


# Database Settings
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': os.environ.get('DATABASE_ENGINE'),
        'NAME': os.environ.get('DATABASE_NAME'),
        'USER': os.environ.get('DATABASE_USER'),
        'PASSWORD': os.environ.get('DATABASE_PASSWORD'),
        'HOST': os.environ.get('DATABASE_HOST'),
        'PORT': int(os.environ.get('DATABASE_PORT', 5432))
    }
}


# Celery Settings
# https://docs.celeryq.dev/en/stable/userguide/configuration.html

BROKER_URL = os.environ.get('CELERY_BROKER_URL')
CELERY_RESULT_BACKEND = BROKER_URL
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERYD_TASK_TIME_LIMIT = 5 * 60
CELERYD_TASK_SOFT_TIME_LIMIT = 60


# Django Email Settings
# https://docs.djangoproject.com/en/4.2/topics/email/

EMAIL_BACKEND = 'django.core.mail.backends.smpt.EmailBackend'
EMAIL_HOST = os.environ.get('EMAIL_HOST', '')
EMAIL_PORT = os.environ.get('EMAIL_PORT', '')
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', '')
EMAIL_USE_TLS = os.environ.get('EMAIL_USE_TLS', '')
EMAIL_USE_SSL = os.environ.get('EMAIL_USE_SSL', '')


# Logging configuration
# https://docs.djangoproject.com/en/4.2/ref/logging/

# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'filters': {
#         'require_debug_false': {
#             '()': 'django.utils.log.RequireDebugFalse',
#         },
#     },
#     'formatters': {
#         'verbose': {
#             'format': (
#                 '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
#             )
#         },
#     },
#     'handlers': {
#         'mail_admins': {
#             'level': 'ERROR',
#             'class': 'django.utils.log.AdminEmailHandler',
#             'filters': ['require_debug_false'],
#             'email_backend': EMAIL_BACKEND
#         },
#         'console': {
#             'level': 'DEBUG',
#             'class': 'logging.StreamHandler',
#             'filters': ['require_debug_false'],
#             'format': 'verbose'
#         },
#     },
#     'loggers': {
#         'django.request': {
#             'handlers': ['console', 'mail_admins'],
#             'level': 'ERROR',
#             'propagate': True
#         },
#         'django.security.DisallowedHost': {
#             'level': 'ERROR',
#             'handlers': ['console', 'mail_admins'],
#             'propagate': True
#         },
#         'django.db.backends': {}
#     },
# }