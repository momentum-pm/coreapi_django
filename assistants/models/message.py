from utils import models


class Message(models.CreatableModel):
    class Meta:
        ordering = ["-created_at"]

    is_response = models.BooleanField(default=False)
    thread = models.ForeignKey(
        to="Thread",
        related_name="messages",
        on_delete=models.CASCADE,
    )
    remote_uuid = models.TextField()
    content = models.TextField()
    files = models.ManyToManyField(to="files.File", blank=True)

    def pre_save(self, in_create=False, in_bulk=False, index=None) -> None:
        if in_create and not self.remote_uuid:
            from utils.llm import llm
            from .assistant import Assistant
            from .run import Run

            if self.thread.runs.exists():
                run = self.thread.runs.first()
            else:
                # TODO select assistant in a better way!
                assistant = Assistant.objects.first()
                instructions_for_run = assistant.get_instructions_for_run(
                    self.thread.member
                )
                run = Run.objects.create(
                    thread=self.thread,
                    assistant=assistant,
                    instructions=instructions_for_run,
                )
                remote_run_id = llm.create_run_id(
                    thread_id=self.thread.remote_uuid,
                    assistant_id=assistant.remote_uuid,
                    instructions=instructions_for_run,
                )
                run.remote_uuid = remote_run_id
                run.save()
            file_paths = []
            message_id = llm.get_message_id(
                content=self.content,
                file_paths=file_paths,
                thread_id=self.thread.remote_uuid,
            )
            self.remote_uuid = message_id

        return super().pre_save(in_create, in_bulk, index)
