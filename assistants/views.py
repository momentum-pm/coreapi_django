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

            first_message = thread.messages.first()
            if first_message and not first_message.is_response:
                run = thread.runs.first()
                run_status = llm.get_run_status(run.remote_uuid, thread.remote_uuid)
                if run_status in ["queued", "in_progress"]:
                    print("PASSING", run_status)
                    pass
                elif run_status in ["completed"]:
                    print("REQUESTING", run_status)
                    last_message = llm.get_last_message(thread_id=thread.remote_uuid)

                    for message in last_message:
                        message_id = message.id
                        if (
                            models.Message.objects.filter(
                                remote_uuid=message_id
                            ).exists()
                            is False
                        ):
                            content = message.content[0].text.value
                            if len(content) > 3:
                                models.Message.objects.create(
                                    remote_uuid=message.id,
                                    content=content,
                                    is_response=True,
                                    thread=thread,
                                )
                            else:
                                models.Message.objects.create(
                                    remote_uuid=message.id,
                                    content=message.__str__(),
                                    is_response=True,
                                    thread=thread,
                                )
                elif run_status in ["cancelling", "cancelled", "expired", "failed"]:
                    models.Message.objects.create(
                        remote_uuid="-------------",
                        content="Sorry, some error eccured, please try again",
                        is_response=True,
                        thread=thread,
                    )
                elif run_status in ["requires_action"]:
                    print("SOME ACTION NEEDED")
                    print(message)
            return thread.messages.all()
        else:
            return super().get_base_queryset()

    def get_thread(self):
        return self.get_object(
            queryset=models.Thread.objects.all(), keyword="thread_pk"
        )
