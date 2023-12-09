from utils import serializers

from . import models


class AssistantBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Assistant
        fields = [
            "id",
            "member",
        ]


class ThreadCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Thread
        fields = ["member"]


class MessageCreateSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ["thread", "content", "files"]
        model = models.Message


class MessgeRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ["id", "created_at", "thread", "content"]
        model = models.Message
