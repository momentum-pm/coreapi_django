from utils import models


class TimelineItem(models.CreatableModel):
    UPCOMMING = "upcomming"
    ONGOING = "ongoing"
    PASSED = "passed"
    STATE_CHOICES = (
        (UPCOMMING, UPCOMMING),
        (ONGOING, ONGOING),
        (PASSED, PASSED),
    )
    title = models.CharField(max_length=255)
    start = models.DateField(null=True, blank=True, default=None)
    end = models.DateField(null=True, blank=True, default=None)
    state = models.CharField(choices=STATE_CHOICES, default=UPCOMMING)
    goal = models.ForeignKey(
        to="Goal",
        related_name="timeline",
        on_delete=models.CASCADE,
    )
