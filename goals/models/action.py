from utils import models


class Action(models.CreatableModel):
    class Meta:
        ordering = ["-created_at"]

    summary = models.TextField()
    goal = models.ForeignKey(
        to="Goal",
        related_name="actions",
        on_delete=models.CASCADE,
    )
    person = models.ForeignKey(
        to="Person",
        related_name="actions",
        on_delete=models.CASCADE,
    )
