from django.urls import path

from instagram.messenger.consumers import MessengerConsumer


websocket_urlpatterns = [
    path('ws/messages/<uuid:uuid>/', MessengerConsumer.as_asgi(), name='inbox')
]