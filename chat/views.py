from utils import views, responses, permissions
from . import serializers, models
from .actions import Actions


class ChatsView(views.CreateModelMixin):
    request_serializer = serializers.ChatCreateSerializer


class MessagesView(views.CreateModelMixin, views.PaginateModelMixin):
    filter_lookups = {"chat": "chat"}
    request_serializer = {"create": serializers.MessageCreateSerializer}
    response_serializer = {"paginate": serializers.MessgeRetrieveSerializer}
