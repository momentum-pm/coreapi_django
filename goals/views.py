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
    filter_lookups = {
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

    @views.action(methods=["post"], detail=True)
    def create_assistant(self, *args, **kwargs):
        try:
            obj = self.get_object()
            models.AnalyzerAssistant.objects.filter(goal=obj).delete()
            models.AnalyzerAssistant.objects.create(goal=obj)
            return responses.Ok(message=self.get_delete_message(obj))
        except responses.BadRequest as response:
            return response


class GoalsInitiateView(
    views.RetrieveModelMixin,
):
    permission_classes = [permissions.AllowAny]
    base_queryset = models.Goal.objects.all()

    response_serializer = {
        "retrieve": serializers.GoalInitiateSerializer,
    }


class GoalsRunView(
    views.RetrieveModelMixin,
):
    permission_classes = [permissions.AllowAny]
    base_queryset = models.Goal.objects.all()

    response_serializer = {
        "retrieve": serializers.GoalRunSerializer,
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
    filter_lookups = {
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


class PeopleView(views.CreateModelMixin):
    permission_classes = [permissions.IsAuthenticated]
    base_queryset = models.Person.objects.all()
    request_serializer = serializers.PersonCreateSerializer

    def get_serializer_context(self):
        super_context = super().get_serializer_context()
        super_context.update(user=self.request.user)
        return super_context
