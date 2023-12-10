from utils import serializers

from . import models
from assistants.serializers import BaseMemberSerializer


class DependencyNestedSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Dependency
        fields = ["summary", "target"]

    def validate(self, attrs):
        attrs = super().validate(attrs)
        attrs.update(source=self.context.get("source"))
        return attrs


class PersonRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Person
        fields = ["id", "name", "about"]


class ResponsibilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Responsibility
        fields = ["id", "person", "summary", "status"]

    person = PersonRetrieveSerializer()


class ActionCompactSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Action
        fields = ["id", "summary", "created_at", "person"]

    person = PersonRetrieveSerializer()


class MetricSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Metric
        fields = ["id", "name", "summary"]


class MetricValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.MetricValue
        fields = ["id", "created_at", "value", "metric"]

    metric = serializers.SerializerMethodField()

    def get_metric(self, obj):
        return obj.metric.name


class RelatedGoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Goal
        fields = ["name", "summary"]


class DependencyTargetSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Dependency
        fields = ["summary", "target"]

    target = RelatedGoalSerializer()


class DependencySourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Dependency
        fields = ["summary", "source"]

    source = RelatedGoalSerializer()


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Notification
        fields = ["sender", "information", "created_at"]

    sender = BaseMemberSerializer()


class GoalFullRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Goal
        fields = [
            "id",
            "name",
            "summary",
            "start",
            "end",
            "state",
            "notifications",
            "last_actions",
            "responsibilities",
            "metrics",
            "latest_metric_values",
            "dependencies",
            "dependents",
            "subgoals",
            "parent",
        ]

    notifications = NotificationSerializer(many=True)
    last_actions = ActionCompactSerializer(many=True)
    responsibilities = ResponsibilitySerializer(many=True)
    metrics = MetricSerializer(many=True)
    latest_metric_values = MetricValueSerializer(many=True)
    dependencies = DependencySourceSerializer(many=True)
    dependents = DependencyTargetSerializer(many=True)
    subgoals = RelatedGoalSerializer(many=True)
    parent = RelatedGoalSerializer(many=True)


class GoalCreateEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Goal
        fields = [
            "owner",
            "name",
            "summary",
            "metrics",
            "dependencies",
            "dependents",
            "subgoals",
            "parent",
        ]


class GoalRunSerializer(GoalFullRetrieveSerializer):
    class Meta:
        model = models.Goal
        fields = [
            "start",
            "end",
            "notifications",
            "state",
            "last_actions",
            "responsibilities",
            "latest_metric_values",
        ]


class GoalInitiateSerializer(GoalFullRetrieveSerializer):
    class Meta:
        model = models.Goal
        fields = [
            "id",
            "name",
            "summary",
            "metrics",
            "dependencies",
            "dependents",
            "subgoals",
            "parent",
        ]


class GoalBaseRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Goal
        fields = [
            "id",
            # "assistant",
            "name",
            "summary",
            # "entities",
        ]

    # assistant = AssistantBaseSerializer()


## ENtitiy Serializers


class EntityCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Entity
        fields = [
            "summary",
            "data",
        ]

    def create(self, validated_data):
        validated_data.update(creator=self.context.get("request").user)
        super().create(validated_data)


class EntityBaseRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Entity
        fields = [
            "id",
            "summary",
            "data",
        ]


class EntityFullRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Entity
        fields = [
            "id",
            "summary",
            "data",
            "goals",
        ]

    goals = GoalBaseRetrieveSerializer(many=True)


### Effect serializers
class EffectRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Effect
        fields = [
            "id",
            "created_at",
        ]


class EffectCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Effect
        fields = ["summary", "data", "goal", "entity"]


class PersonCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Person
        fields = ["about"]

    def validate(self, attrs):
        attrs = super().validate(attrs)
        user = self.context.get("user")
        attrs.update(user=user)
        return attrs


# goal: developing a website (responsibiliets: Reza should manage the interface between Dave and max)
# subgoal 1: develop the backend start :1 end 10  (responsibiliets: Dave should create the db)
# subgoal 2: develop the frontend start: 11, end :15->20 (responsibilites: Max should create the login page)


## {proerties_changes, responsibilities_changes, start_change, end_change}
##
