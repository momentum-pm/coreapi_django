from utils import models


class Message(models.CreatableModel):
    class Meta:
        ordering = ["-created_at"]

    USER = "user"
    ASSISTANT = "assistant"
    NOTIFICATION = "notification"
    CALL = "call"
    TYPE_CHOICES = (
        (USER, USER),
        (ASSISTANT, ASSISTANT),
        (NOTIFICATION, NOTIFICATION),
        (CALL, CALL),
    )

    def get_default_type():
        return Message.USER

    type = models.CharField(choices=TYPE_CHOICES, default=get_default_type)
    is_response = models.BooleanField(default=False)

    thread = models.ForeignKey(
        to="Thread",
        related_name="messages",
        on_delete=models.CASCADE,
    )
    remote_uuid = models.TextField()
    content = models.TextField(null=True, blank=True, default=None)
    files = models.ManyToManyField(to="files.File", blank=True)

    def pre_save(self, in_create=False, in_bulk=False, index=None) -> None:
        if in_create and not self.remote_uuid:
            from utils.llm import llm

            file_paths = []
            message_id = llm.get_message_id(
                content=self.content,
                file_paths=file_paths,
                thread_id=self.thread.remote_uuid,
            )
            self.remote_uuid = message_id

        return super().pre_save(in_create, in_bulk, index)
