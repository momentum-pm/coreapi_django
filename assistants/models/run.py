from utils import models


class Run(models.CreatableModel):
    class Meta:
        ordering = ["-created_at"]

    QUEUED = "queued"
    remote_uuid = models.TextField()
    thread = models.ForeignKey(
        to="Thread", related_name="runs", on_delete=models.CASCADE
    )
    state = models.CharField(max_length=20, default=QUEUED)
    assistant = models.ForeignKey(
        to="Assistant", related_name="runs", on_delete=models.CASCADE
    )
    instructions = models.TextField()
