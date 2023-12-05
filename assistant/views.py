from utils import views, responses, permissions
from . import serializers, models
from .actions import Actions


class GoalsView(
    views.CreateModelMixin,
    views.BulkCreateModelMixin,
    views.ListModelMixin,
    views.RetrieveModelMixin,
    views.DeleteModelMixin,
    views.EditModelMixin,
):
    permission_classes = [permissions.AllowAny]
    base_queryset = models.Goal.objects.all()

    ordering_choices = {
        "oldest": "created_at",
        "newest": "-created_at",
    }
    filter_lookups: {
        "owner": "owner",
    }
    request_serializer = {
        "create": serializers.GoalCreateEditSerializer,
        "bulk_create": serializers.GoalCreateEditSerializer,
        "edit": serializers.GoalCreateEditSerializer,
    }
    response_serializer = {
        "list": serializers.GoalBaseRetrieveSerializer,
        "retrieve": serializers.GoalFullRetrieveSerializer,
    }


class EntitiesView(
    views.CreateModelMixin,
    views.BulkCreateModelMixin,
    views.ListModelMixin,
    views.RetrieveModelMixin,
    views.DeleteModelMixin,
):
    permission_classes = [permissions.AllowAny]
    base_queryset = models.Entity.objects.all()

    ordering_choices = {
        "oldest": "created_at",
        "newest": "-created_at",
    }
    filter_lookups: {
        "types": "type__in",
        "from": "created_at__gte",
        "to": "created_at__lte",
    }
    request_serializer = {
        "create": serializers.EntityCreateSerializer,
        "bulk_create": serializers.EntityCreateSerializer,
    }
    response_serializer = {
        "list": serializers.EntityBaseRetrieveSerializer,
        "retrieve": serializers.EntityFullRetrieveSerializer,
    }


class EffectsView(
    views.CreateModelMixin,
    views.BulkCreateModelMixin,
    views.ListModelMixin,
    views.RetrieveModelMixin,
    views.DeleteModelMixin,
):
    permission_classes = [permissions.AllowAny]
    base_queryset = models.Effect.objects.all()
    ordering_choices = {
        "oldest": "created_at",
        "newest": "-created_at",
    }
    filter_lookups: {
        "goal": "goal",
        "entity": "entity",
        "from": "created_at__gte",
        "to": "created_at__lte",
    }
    request_serializer = {
        "create": serializers.EffectCreateSerializer,
        "bulk_create": serializers.EffectCreateSerializer,
    }
    response_serializer = {
        "list": serializers.EffectRetrieveSerializer,
        "retrieve": serializers.EffectRetrieveSerializer,
    }
