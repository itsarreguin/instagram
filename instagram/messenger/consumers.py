import json
from typing import Any, Type

from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync

from instagram.account.models import User
from instagram.messenger.models import Inbox, Message
from instagram.messenger.serializers import MessageSerializer


class MessengerConsumer(WebsocketConsumer):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.model = Inbox

    def connect(self) -> None:
        self.current_user = self.scope['user']
        self.inbox_uuid = self.scope['url_route']['kwargs']['uuid']
        self.inbox = self.model.objects.get(uuid=self.inbox_uuid)
        self.room_group_name = f'inbox-{self.inbox_uuid}'

        self.accept()

        if self.current_user.is_authenticated:
            async_to_sync(self.channel_layer.group_add)(
                self.room_group_name, self.channel_name
            )

    def receive(self, text_data: str = None, bytes_data: bytes = None) -> None:
        json_data = json.loads(text_data)

        if not self.current_user.is_authenticated:
            return

        message = self.save_message(json_data['receiver'], json_data['message'])
        async_to_sync(self.channel_layer.group_send)(self.room_group_name, {
            'type': 'send.message',
            'message' : self.serialize_data(message)
        })

    def disconnect(self, code: int = None) -> None:
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )
        self.close(code)

    def send_message(self, event: dict[str, Any]) -> None:
        self.send(text_data=json.dumps(event))

    def save_message(self, username: str, message: str) -> Type[Message]:
        receiver = User.objects.get(username=username)
        new_message = Message.objects.create(
            inbox=self.inbox,
            sender=self.current_user,
            receiver=receiver,
            body=message
        )
        return new_message

    def serialize_data(self, instance: Message) -> dict[str, Any]:
        serializer = MessageSerializer(instance=instance)
        return serializer.data