from utils import models


class Action(models.CreatableModel):
    class Meta:
        ordering = ["-created_at"]

    summary = models.TextField()


"""
Action: {
time,
summary,
responsibilites_effects: [{"responsibility","state"}]
created_records: [ {"property","value"}]
}
"""
#
