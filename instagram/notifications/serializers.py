from typing import Any, Dict, Type

from instagram.notifications.models import Notification


def notification_serializer(instance: Type[Notification]) -> Dict[str, Any]:
    receiver_picture = instance.receiver.profile.picture
    sender_picture = instance.sender.profile.picture

    return {
        'id': instance.id,
        'category': instance.category,
        'slug': instance.slug,
        'sender': {
            'id': instance.sender.id,
            'username': instance.sender.username,
            'first_name': instance.sender.first_name,
            'last_name': instance.sender.last_name,
            'profile': {
                'picture': sender_picture.url if sender_picture else None,
            }
        },
        'receiver': {
            'id': instance.receiver.id,
            'username': instance.receiver.username,
            'first_name': instance.receiver.first_name,
            'last_name': instance.receiver.last_name,
            'profile': {
                'picture': receiver_picture.url if receiver_picture else None
            }
        },
        'is_read': instance.is_read,
        'object_id': instance.object_id,
        'object_slug': instance.object_slug,
        'created': instance.formated_timestamp
    }