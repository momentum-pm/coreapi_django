from utils import models


class Responsibility(models.CreatableModel):
    UPCOMMING = "upcomming"
    ONGOING = "ongoing"
    PASSED = "passed"
    STATE_CHOICES = (
        (UPCOMMING, UPCOMMING),
        (ONGOING, ONGOING),
        (PASSED, PASSED),
    )
    state = models.CharField(choices=STATE_CHOICES, default=UPCOMMING)

    people = models.ManyToManyField(
        to="Person", related_name="responsibilities", blank=True
    )
    summary = models.TextField()
    goal = models.ForeignKey(
        to="Goal",
        related_name="responsibilites",
        on_delete=models.CASCADE,
    )
    actions = models.ManyToManyField(
        to="Action",
        related_name="responsibilities",
        blank=True,
    )

    @property
    def latest_action(self):
        self.actions().first()