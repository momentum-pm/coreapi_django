from utils import models


class Call(models.CreatableModel):
    class Meta:
        ordering = ["-created_at"]

    question = models.TextField(null=True, blank=True, default=None)
    func = models.ForeignKey(
        to="Function", on_delete=models.CASCADE, related_name="calls"
    )
    message = models.ForeignKey(
        to="Message", on_delete=models.CASCADE, related_name="calls"
    )
    arguments = models.JSONField()
    remote_uuid = models.TextField()
    output = models.TextField(null=True, blank=True, default=None)

    # goal = models.ForeignKey(
    #     to="Goal",
    #     related_name="actions",
    #     on_delete=models.CASCADE,
    # )
    # person = models.ForeignKey(
    #     to="Person",
    #     related_name="actions",
    #     on_delete=models.CASCADE,
    # )
