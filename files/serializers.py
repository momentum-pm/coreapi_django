from rest_framework import serializers
from . import models


class FileUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.File
        fields = ["file"]


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.File
        fields = ["file", "uuid", "id", "name", "format", "size"]
