from utils import views, responses
from . import serializers, models, messages
from rest_framework.permissions import AllowAny, IsAuthenticated


class FilesView(views.BaseViewSet):
    permission_classes = [AllowAny]

    request_serializer = {
        "upload": serializers.FileUploadSerializer,
    }
    response_serializer = {
        "upload": serializers.FileSerializer,
        "info": serializers.FileSerializer,
    }

    @views.action(methods=["post"], detail=False)
    def upload(self, request):
        try:
            RequestSerializer = self.get_request_serializer()
            ResponseSerializer = self.get_response_serializer()
            context = self.get_serializer_context()
            request_serializer = RequestSerializer(context=context, data=request.data)
            request_serializer.is_valid(raise_exception=True)
            request_serializer.save()
            instance = request_serializer.instance
            response_serializer = ResponseSerializer(instance, context=context)
            return responses.Created(data=response_serializer.data)
        except responses.BadRequest as response:
            return response

    @views.action(methods=["get"], detail=False)
    def info(self, request, uuid):
        try:
            ResponseSerializer = self.get_response_serializer()
            context = self.get_serializer_context()
            file = models.File.objects.get_by_uuid(uuid)
            response_serializer = ResponseSerializer(file, context=context)
            return responses.Created(data=response_serializer.data)
        except models.File.DoesNotExist:
            return responses.NotFound(message=self.get_not_found_message())

    @views.action(methods=["delete"], detail=False)
    def delete(self, request, uuid):
        try:
            file = models.File.objects.get_by_uuid(uuid)
            file.delete()
            return responses.Ok(message=messages.file_deleted_message)
        except models.File.DoesNotExist:
            return responses.NotFound(message=self.get_not_found_message())
