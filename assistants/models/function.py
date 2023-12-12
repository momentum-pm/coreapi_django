from utils import models


class Function(models.Model):
    specification = models.JSONField()
    assistant = models.ForeignKey(
        to="Assistant",
        related_name="functions",
        on_delete=models.CASCADE,
    )

    def __str__(self) -> str:
        return self.assistant.__class__.__name__ + "." + self.specification.get("name")
