from utils import serializers

from . import models


class ChatCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Chat
        fields = ["members"]

    members = serializers.PrimaryKeyRelatedField(
        many=True, queryset=models.Member.objects.all()
    )

    def create(self, validated_data):
        members = validated_data.pop("members")
        chat = super().create(validated_data)
        for member in members:
            models.Membership.objects.create(chat=chat, member=member)
        return chat


class MessageCreateSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ["member", "chat", "content"]
        model = models.Message

    def create(self, validated_data):
        message = super().create(validated_data)
        chat = message.chat
        chat.create_next_message()
        return message


class MessgeRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ["id", "created_at", "member", "content"]
        model = models.Message

