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


class GoalFullRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Goal
        fields = [
            "id",
            "name",
            "summary",
            "dependencies",
            "properties",
            "entities",
            "children",
        ]


from assistants.serializers import AssistantBaseSerializer


class GoalBaseRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Goal
        fields = [
            "id",
            "assistant",
            "name",
            "summary",
            "entities",
        ]

    assistant = AssistantBaseSerializer()


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
