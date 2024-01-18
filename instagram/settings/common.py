# Instagram common settings module
import os

from pathlib import Path

from dotenv import load_dotenv


PACKAGE_DIR = Path(__file__).resolve().parent.parent

BASE_DIR = PACKAGE_DIR.parent

load_dotenv(os.path.join(BASE_DIR, '.env'))

DEBUG = os.environ['DEBUG']


# Application definition

DJANGO_APPS = [
    'daphne.apps.DaphneConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'channels.apps.ChannelsConfig',
]

PROJECT_APPS = [
    'instagram.core.apps.CoreConfig',
    'instagram.account.apps.AccountConfig',
    'instagram.posts.apps.PostsConfig',
    'instagram.notifications.apps.NotificationsConfig',
    'instagram.messenger.apps.MessengerConfig'
]

THIRD_APPS = []

INSTALLED_APPS = DJANGO_APPS + PROJECT_APPS + THIRD_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'instagram.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'instagram.notifications.context_processors.readed_notifications',
                'instagram.posts.context_processors.post_form',
                'instagram.posts.context_processors.collections',
                'instagram.posts.context_processors.post_liked',
            ],
        },
    },
]

WSGI_APPLICATION = 'instagram.wsgi.application'
ASGI_APPLICATION = 'instagram.asgi.application'

# Auth user model definition
AUTH_USER_MODEL = 'account.User'


# Redis Settings
REDIS_HOST = os.environ.get('REDIS_HOST', '127.0.0.1')
REDIS_PORT = int(os.environ.get('REDIS_PORT', 6379))


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Django Channels config
# https://channels.readthedocs.io/en/latest/topics/channel_layers.html

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            'hosts': [(REDIS_HOST, REDIS_PORT)],
        },
    },
}


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static/')
]

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')


# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# Authetication redirects -----------------------

LOGIN_URL = 'account:login'
LOGIN_REDIRECT_URL = 'account:feed'
LOGOUT_REDIRECT_URL = LOGIN_URL


# Email settings
# https://docs.djangoproject.com/en/4.2/topics/email/

DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL')