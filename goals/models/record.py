from utils import models


class Record(models.CreatableModel):
    class Meta:
        ordering = ["-created_at"]

    summary = models.TextField(blank=True, null=True, default=None)
    property = models.ForeignKey(
        to="Property",
        related_name="+",
        on_delete=models.CASCADE,
    )
    goal = models.ForeignKey(
        to="Goal",
        related_name="history",
        on_delete=models.CASCADE,
    )
    data = models.JSONField(blank=True, null=True, default=None)

    def __str__(self) -> str:
        return self.summary
