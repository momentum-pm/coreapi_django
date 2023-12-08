from utils import models


class Member(models.Model):
    PERSON = "Person"
    ASSISTANT = "Assistant"
    SYSTEM = "System"

    ROLE_CHOICES = (
        (ASSISTANT, ASSISTANT),
        (PERSON, PERSON),
        (SYSTEM, SYSTEM),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)


class Chat(models.Model):
    members = models.ManyToManyField(
        to="Member",
        blank=True,
        related_name="chats",
        through="Membership",
    )

    def create_next_message(self):
        from utils.llm import LLM

        response = LLM.from_chat(
            prompt="You are a an assistant who in a polite tone",
            chat=self,
        )
        from chat.models import Message
        from assistant.models import Assistant

        assistant = Assistant.objects.first()
        Message.objects.create(member=assistant.member, content=response, chat=self)


class Membership(models.CreatableModel):
    member = models.ForeignKey(
        to="Member",
        related_name="memberships",
        on_delete=models.CASCADE,
    )
    chat = models.ForeignKey(
        to="Chat",
        related_name="memberships",
        on_delete=models.CASCADE,
    )


class Message(models.CreatableModel):
    class Meta:
        ordering = ["-created_at"]

    member = models.ForeignKey(
        to="Member",
        related_name="messages",
        on_delete=models.CASCADE,
    )
    chat = models.ForeignKey(
        to="Chat",
        related_name="messages",
        on_delete=models.CASCADE,
    )

    content = models.TextField()
