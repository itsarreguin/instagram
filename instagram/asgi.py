"""
ASGI config for Instagram project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter

from dotenv import load_dotenv

from instagram import routing


load_dotenv()

os.environ.setdefault('DJANGO_SETTINGS_MODULE', os.environ['PROJECT_SETTINGS'])

application = ProtocolTypeRouter(
    {
        'http': get_asgi_application(),
        'websocket': AuthMiddlewareStack(
            URLRouter(routing.websocket_urlpatterns)
        )
    }
)