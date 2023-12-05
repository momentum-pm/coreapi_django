from utils import models


class Chat(models.Model):
    person = models.ForeignKey(
        to="people.Person",
        related_name="chats",
        on_delete=models.CASCADE,
    )


class Message(models.CreatableModel):
    class Meta:
        ordering = ["-created_at"]

    PERSON = "Person"
    ASSISTANT = "Assistant"

    ROLE_CHOICES = (
        (ASSISTANT, ASSISTANT),
        (PERSON, PERSON),
    )
    content = models.TextField()
    role = models.CharField(choices=ROLE_CHOICES)
    chat = models.ForeignKey(
        to="Chat",
        related_name="messages",
        on_delete=models.CASCADE,
    )
