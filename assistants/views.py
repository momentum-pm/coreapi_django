from utils import models, views, responses, permissions
from . import serializers, models
from .actions import Actions


class ThreadsView(views.CreateModelMixin):
    request_serializer = serializers.ThreadCreateSerializer


class MessagesView(views.CreateModelMixin, views.PaginateModelMixin):
    permission_classes = [permissions.AllowAny]
    request_serializer = {"create": serializers.MessageCreateSerializer}
    response_serializer = {"paginate": serializers.MessgeRetrieveSerializer}

    def get_base_queryset(self):
        if self.action == "paginate":
            thread = self.get_thread()
            from utils.llm import llm

            data = llm.get_messages(thread_id=thread.remote_uuid)
            for message in data:
                message_id = message.id
                if models.Message.objects.filter(remote_uuid=message_id).exists():
                    pass
                else:
                    models.Message.objects.create(
                        remote_uuid=message.id,
                        content=message.content[0].text.value,
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
