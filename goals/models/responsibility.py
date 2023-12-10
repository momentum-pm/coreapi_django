from utils import models


class Responsibility(models.CreatableModel):
    summary = models.TextField()
    status = models.TextField()
    person = models.ForeignKey(
        to="Person", related_name="responsibilities", on_delete=models.CASCADE
    )
    goal = models.ForeignKey(
        to="Goal",
        related_name="responsibilities",
        on_delete=models.CASCADE,
    )
