from utils import serializers

from . import models


class AssistantBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Assistant
        fields = [
            "id",
            "member",
        ]


class BaseMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Member
        feilds = ["id", "name"]


class ThreadCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Thread
        fields = ["member"]


class MessageCreateSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ["thread", "content", "files", "assistant"]
        model = models.Message

    assistant = serializers.PrimaryKeyRelatedField(
        queryset=models.Assistant.objects.all()
    )

    def create(self, validated_data):
        from assistants.models import Run

        assistant = validated_data.pop("assistant")
        thread = validated_data.get("assistant")
        if thread.runs.exists():
            current_run = self.thread.runs.first()
        if not current_run or current_run.assistant != assistant:
            instructions_for_run = assistant.get_instructions_for_run(thread.member)
            run = Run.objects.create(
                thread=thread,
                assistant=assistant,
                instructions=instructions_for_run,
            )
            from utils.llm import llm

            remote_run_id = llm.create_run_id(
                thread_id=thread.remote_uuid,
                assistant_id=assistant.remote_uuid,
                instructions=instructions_for_run,
            )
            run.remote_uuid = remote_run_id
            run.save()
        return super().create(validated_data)


class MessgeRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ["id", "created_at", "thread", "content"]
        model = models.Message
