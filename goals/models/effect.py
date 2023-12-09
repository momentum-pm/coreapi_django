from utils import models


class Effect(models.CreatableModel):
    class Meta:
        ordering = ["-created_at"]

    summary = models.TextField()
    data = models.JSONField()
    goal = models.ForeignKey(
        to="Goal",
        related_name="effects",
        on_delete=models.CASCADE,
    )
    entity = models.ForeignKey(
        to="Entity",
        related_name="effects",
        on_delete=models.CASCADE,
    )
