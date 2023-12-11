from utils import models, views, responses, permissions
from . import serializers, models
from .actions import Actions


class ThreadsView(views.CreateModelMixin, views.ListModelMixin):
    permission_classes = [permissions.AllowAny]

    base_queryset = models.Thread.objects.all()
    request_serializer = serializers.ThreadCreateSerializer
    response_serializer = serializers.ThreadListSerializer
    filter_lookups = {
        "person": "member__person",
    }


class AssistantsView(views.ListModelMixin):
    permission_classes = [permissions.AllowAny]
    base_queryset = models.Assistant.objects.all()
    response_serializer = serializers.AssistantBaseSerializer


class MessagesView(views.CreateModelMixin, views.ListModelMixin):
    permission_classes = [permissions.AllowAny]
    request_serializer = {"create": serializers.MessageCreateSerializer}
    response_serializer = {"list": serializers.MessgeRetrieveSerializer}
    filter_lookups = ["create_at__lt", "created_at__gt"]

    def get_base_queryset(self):
        if self.action == "list":
            thread = self.get_thread()
            from utils.llm import llm

            data = llm.get_messages(thread_id=thread.remote_uuid)
            for message in data:
                message_id = message.id
                if models.Message.objects.filter(remote_uuid=message_id).exists():
                    pass
                else:
                    content = message.content[0].text.value
                    if len(content) > 3:
                        models.Message.objects.create(
                            remote_uuid=message.id,
                            content=content,
                            is_response=True,
                            thread=thread,
                        )
            return thread.messages.all()
        else:
            return super().get_base_queryset()

    def get_thread(self):
        return self.get_object(
            queryset=models.Thread.objects.all(), keyword="thread_pk"
        )
