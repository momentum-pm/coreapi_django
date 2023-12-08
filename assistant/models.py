from utils import models


class Assistant(models.Model):
    state = models.TextField()
    member = models.OneToOneField(
        to="chat.Member",
        on_delete=models.CASCADE,
        related_name="assistant",
    )

    def pre_save(self, in_create=False, in_bulk=False, index=None) -> None:
        if in_create:
            from chat.models import Member

            member = Member.objects.create(role=Member.ASSISTANT)
            self.member = member
        return super().pre_save(in_create, in_bulk, index)

    def __str__(self) -> str:
        return f"{self.goal.name}'s assistant"


class Goal(models.CreatableModel):
    owner = models.ForeignKey(
        to="people.Person",
        related_name="owned_goals",
        on_delete=models.CASCADE,
    )
    assistant = models.OneToOneField(to="Assistant", on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    summary = models.TextField(blank=True)
    parent = models.ForeignKey(
        to="Goal",
        related_name="children",
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

    def pre_save(self, in_create=False, in_bulk=False, index=None) -> None:
        if in_create:
            assistant = Assistant.objects.create(state="initial")
            self.assistant = assistant
        return super().pre_save(in_create, in_bulk, index)

    def __str__(self) -> str:
        return self.name


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


class Property(models.Model):
    name = models.CharField(max_length=255)
    summary = models.TextField()

    def __str__(self) -> str:
        return self.name


class Record(models.CreatableModel):
    class Meta:
        ordering = ["-created_at"]

    summary = models.TextField(blank=True, null=True, default=None)
    property = models.ForeignKey(
        to="Property",
        related_name="+",
        on_delete=models.CASCADE,
    )
    goal = models.ForeignKey(
        to="Goal",
        related_name="history",
        on_delete=models.CASCADE,
    )
    data = models.JSONField(blank=True, null=True, default=None)

    def __str__(self) -> str:
        return self.summary


class EntityType(models.Model):
    name = models.CharField(max_length=255)
    summary = models.TextField()

    def __str__(self) -> str:
        return self.name


class Entity(models.CreatableModel):
    class Meta:
        ordering = ["-created_at"]

    creator = models.ForeignKey(
        to="people.Person",
        related_name="created_entities",
        on_delete=models.CASCADE,
    )
    type = models.ForeignKey(
        to="EntityType",
        related_name="entities",
        null=True,
        blank=True,
        default=None,
        on_delete=models.SET_NULL,
    )
    summary = models.TextField(blank=True)
    data = models.JSONField(blank=True)

    def __str__(self) -> str:
        return self.summary


class Effect(models.CreatableModel):
    class Meta:
        ordering = ["-created_at"]

    summary = models.TextField()
    data = models.JSONField()
    goal = models.ForeignKey(
        to="Goal",
        related_name="effects",
        on_delete=models.CASCADE,
    )
    entity = models.ForeignKey(
        to="Entity",
        related_name="effects",
        on_delete=models.CASCADE,
    )
