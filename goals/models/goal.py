from utils import models


class Goal(models.CreatableModel):
    owner = models.ForeignKey(
        to="Person",
        related_name="owned_goals",
        on_delete=models.CASCADE,
    )
    UPCOMMING = "upcomming"
    ONGOING = "ongoing"
    PASSED = "passed"
    STATE_CHOICES = (
        (UPCOMMING, UPCOMMING),
        (ONGOING, ONGOING),
        (PASSED, PASSED),
    )
    start = models.DateField(null=True, blank=True, default=None)
    end = models.DateField(null=True, blank=True, default=None)
    state = models.CharField(choices=STATE_CHOICES, default=UPCOMMING)
    name = models.CharField(max_length=255)
    summary = models.TextField(blank=True)
    parent = models.ForeignKey(
        to="Goal",
        related_name="subgoals",
        null=True,
        blank=True,
        default=None,
        on_delete=models.CASCADE,
    )
    dependency_goals = models.ManyToManyField(
        to="Goal",
        related_name="dependent_goals",
        through="Dependency",
    )
    properties = models.ManyToManyField(
        to="Property",
        related_name="goals",
        through="Record",
    )
    entities = models.ManyToManyField(
        to="Entity",
        related_name="goals",
        through="Effect",
    )

    def post_save(self, in_create=False, in_bulk=False, index=None) -> None:
        if in_create:
            from .analyzer_assistant import AnalyzerAssistant

            self.assistant = AnalyzerAssistant.objects.create(goal=self.goal)
        return super().post_save(in_create, in_bulk, index)

    def __str__(self) -> str:
        return self.name
