from utils import models


class Entity(models.CreatableModel):
    class Meta:
        ordering = ["-created_at"]

    creator = models.ForeignKey(
        to="Person",
        related_name="created_entities",
        on_delete=models.CASCADE,
    )
    summary = models.TextField(blank=True)
    data = models.JSONField(blank=True)
    files = models.ManyToManyField(to="files.File", blank=True)

    def __str__(self) -> str:
        return self.summary
