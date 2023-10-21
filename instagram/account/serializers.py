from rest_framework import serializers


class ProfileSerializer(serializers.Serializer):
    picture = serializers.ImageField()


class UserSerializer(serializers.Serializer):
    username = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    profile = ProfileSerializer(read_only=True)