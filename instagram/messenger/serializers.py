from rest_framework import serializers

from instagram.account.serializers import UserSerializer


class MessageSerializer(serializers.Serializer):
    sender = UserSerializer(read_only=True)
    receiver = UserSerializer(read_only=True)
    body = serializers.CharField()
    created = serializers.DateTimeField()