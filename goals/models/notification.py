from utils import models


class Notification(models.CreatableModel):
    is_seen = models.BooleanField(default=False)
    information = models.TextField()
    sender = models.ForeignKey(to="Person", on_delete=models.CASCADE)
    goal = models.ForeignKey(
        to="Goal", on_delete=models.CASCADE, related_name="notifications"
    )

    def __str__(self) -> str:
        return self.information
