from utils import views, responses, permissions
from . import serializers, models
from .actions import Actions


class PeopleView(views.CreateModelMixin):
    permission_classes = [permissions.IsAuthenticated]
    base_queryset = models.Person.objects.all()
    request_serializer = serializers.PersonCreateSerializer

    def get_serializer_context(self):
        super_context = super().get_serializer_context()
        super_context.update(user=self.request.user)
        return super_context
