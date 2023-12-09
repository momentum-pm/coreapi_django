from utils import models


class Responsibility(models.CreatableModel):
    people = models.ManyToManyField(
        to="Person", related_name="responsibilities", blank=True
    )
    summary = models.TextField()
    timeline_item = models.ForeignKey(
        to="TimelineItem",
        related_name="responsibilites",
        on_delete=models.CASCADE,
    )
