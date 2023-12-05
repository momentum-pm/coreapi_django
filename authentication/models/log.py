from utils import models


class Log(models.CreatableModel):
    user = models.ForeignKey(
        to="authentication.User",
        related_name="logs",
        related_query_name="log",
        on_delete=models.CASCADE,
    )
    action = models.ForeignKey(
        to="Action",
        related_name="logs",
        related_query_name="log",
        on_delete=models.CASCADE,
    )
    granted = models.BooleanField(default=True)
