from rest_framework import serializers


class EntryCreateRequestSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    subject = serializers.CharField(max_length=255)
    message = serializers.CharField()


class EntryCreateResponseSerializer(serializers.Serializer):
    user = serializers.CharField(max_length=255)
    subject = serializers.CharField(max_length=255)
    message = serializers.CharField()


class EntryResponseSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255)
    subject = serializers.CharField(max_length=255)
    message = serializers.CharField()


class UserResponseSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255)
    total_message_count = serializers.IntegerField()
    last_entry = serializers.CharField()


class UserListResponseSerializer(serializers.Serializer):
    users = UserResponseSerializer(many=True)
