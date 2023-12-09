from utils import models


class Dependency(models.Model):
    summary = models.TextField()
    source = models.ForeignKey(
        to="Goal",
        related_name="dependents",
        on_delete=models.CASCADE,
    )
    target = models.ForeignKey(
        to="Goal",
        related_name="dependencies",
        on_delete=models.CASCADE,
    )

    def __str__(self) -> str:
        return f"{self.source.__str__()} to {self.target.__str__()}"
