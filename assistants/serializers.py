from utils import serializers

from . import models


class AssistantBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Assistant
        fields = [
            "id",
            "name",
            "member",
        ]


class BaseMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Member
        fields = ["id", "name"]


class ThreadCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Thread
        fields = ["member", "assistant"]


from files.serializers import FileSerializer


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Message
        fields = ["id", "created_at", "content", "files", "type"]

    files = FileSerializer(many=True)


class ThreadListSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Thread
        fields = [
            "id",
            "member",
            "assistant",
            "first_message",
        ]

    first_message = MessageSerializer()
    assistant = AssistantBaseSerializer()


class MessageCreateSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ["thread", "content", "files"]
        model = models.Message

    def create(self, validated_data):
        from assistants.models import Run

        message = super().create(validated_data)

        thread = validated_data.get("thread")
        assistant = thread.assistant
        instructions_for_run = assistant.get_instructions_for_run(thread.member)
        run = Run.objects.create(
            thread=thread,
            assistant=assistant,
            instructions=assistant.instructions + instructions_for_run,
        )
        from utils.llm import llm

        remote_run_id = llm.create_run_id(
            thread_id=thread.remote_uuid,
            assistant_id=assistant.remote_uuid,
            instructions=assistant.instructions + instructions_for_run,
        )
        run.remote_uuid = remote_run_id
        run.save()
        return message


class CallSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Call
        fields = [
            "id",
            "function_name",
            "arguments",
            "output",
            "question",
        ]

    function_name = serializers.SerializerMethodField()

    def get_function_name(self, obj):
        return obj.func.specification.get("name")


class MessageRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        fields = [
            "id",
            "created_at",
            "thread",
            "type",
            "content",
            "calls",
            "call_answered",
        ]
        model = models.Message

    calls = CallSerializer(many=True)
