from utils import models


class Property(models.Model):
    name = models.CharField(max_length=255)
    summary = models.TextField()

    def __str__(self) -> str:
        return self.name
