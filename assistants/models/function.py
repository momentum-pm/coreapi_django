from utils import models


class Function(models.Model):
    specification = models.JSONField()
    assistant = models.ForeignKey(
        to="Assistant",
        related_name="functions",
        on_delete=models.CASCADE,
    )
