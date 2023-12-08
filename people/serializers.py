from utils import serializers

from . import models


class PersonCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Person
        fields = ["about"]

    def validate(self, attrs):
        attrs = super().validate(attrs)
        user = self.context.get("user")
        attrs.update(user=user)
        return attrs
