from utils import serializers

from . import models


class DependencyNestedSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Dependency
        fields = ["summary", "target"]

    def validate(self, attrs):
        attrs = super().validate(attrs)
        attrs.update(source=self.context.get("source"))
        return attrs


class RecordNestedSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Record
        fields = ["data", "summary", "property"]

    def validate(self, attrs):
        attrs = super().validate(attrs)
        attrs.update(goal=self.context.get("goal"))
        return attrs


class GoalCreateEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Goal
        fields = [
            "name",
            "summary",
            "owner",
            # "parent",
            # "records",
            # "dependencies",
        ]

    # dependencies = serializers.ListSerializer(child=DependencyNestedSerializer())
    # records = serializers.ListSerializer(child=RecordNestedSerializer())

    def get_nested_context(self, key) -> dict:
        if key == "dependencies":
            return {"source": self.instance}
        if key == "records":
            return {"goal": self.instance}
        return {}

    def create(self, validated_data):
        instance = super().create(validated_data)
        instance.fill_assistant()
        return instance


class ActionCompactSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Action
        fields = ["id", "summary", "created_at"]


class PersonRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Person
        fields = ["id", "name", "about"]


class ResponsibilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Responsibility
        fields = ["id", "people", "summary", "latest_action", "state"]

    people = PersonRetrieveSerializer(many=True)
    latest_action = ActionCompactSerializer()


class CompactPropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Property
        fields = ["id", "name", "summary"]


class RecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Record
        fields = ["id", "created_at", "summary", "action", "property"]

    property = CompactPropertySerializer()


class GoalFullRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Goal
        fields = [
            "id",
            "name",
            "summary",
            "start",
            "end",
            "responsibilities",
            "last_metrics",
            "subgoals",
            "dependencies",
        ]

    responsibilities = ResponsibilitySerializer(many=True)
    last_metrics = serializers.SerializerMethodField()

    def get_last_metrics(self, obj):
        records = []
        for property in obj.properties.all().distinct():
            record = models.Record.objects.filter(goal=obj, property=property).first()
            records.append(record)
        return RecordSerializer(records, many=True).data

    def get_dependencies(self, obj):
        subgoals = obj.dependencies.all()
        return GoalBaseRetrieveSerializer(
            subgoals, many=True, context=self.context
        ).data


from assistants.serializers import AssistantBaseSerializer, BaseMemberSerializer


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


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Notification
        fields = ["sender", "information", "created_at"]

    sender = BaseMemberSerializer()


# goal: developing a website (responsibiliets: Reza should manage the interface between Dave and max)
# subgoal 1: develop the backend start :1 end 10  (responsibiliets: Dave should create the db)
# subgoal 2: develop the frontend start: 11, end :15->20 (responsibilites: Max should create the login page)


## {proerties_changes, responsibilities_changes, start_change, end_change}
##
