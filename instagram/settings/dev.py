# Instagram development settings module

from instagram.settings.common import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-&4s1p8-rj903ne#vv(h_hig_#$w+v!l%i2o@)&2xjru=le=#zs'

ALLOWED_HOSTS = []

DEBUG = True

INSTALLED_APPS += ['django_extensions']


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

MEDIA_URL = 'media/'