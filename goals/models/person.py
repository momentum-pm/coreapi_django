from utils import models
from assistants.models import Member


class Person(models.Model):
    name = models.CharField(max_length=255)
    about = models.TextField(blank=True)
    user = models.OneToOneField(
        to="authentication.User",
        null=True,
        blank=True,
        default=None,
        related_name="person",
        on_delete=models.CASCADE,
    )
    member = models.OneToOneField(
        to="assistants.Member",
        on_delete=models.CASCADE,
        related_name="person",
    )

    def pre_save(self, in_create=False, in_bulk=False, index=None) -> None:
        if in_create:
            if not self.name:
                self.name = f"{self.user.first_name} {self.user.last_name}"
            self.member = Member.objects.create()
        return super().pre_save(in_create, in_bulk, index)

    def __str__(self) -> str:
        return self.name
