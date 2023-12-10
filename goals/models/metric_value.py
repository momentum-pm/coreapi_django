from utils import models


class MetricValue(models.CreatableModel):
    class Meta:
        ordering = ["-created_at"]

    value = models.TextField()
    metric = models.ForeignKey(
        to="Metric",
        related_name="+",
        on_delete=models.CASCADE,
    )
    goal = models.ForeignKey(
        to="Goal",
        related_name="history",
        on_delete=models.CASCADE,
    )

    def __str__(self) -> str:
        return self.summary
