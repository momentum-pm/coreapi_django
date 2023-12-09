from django.contrib import admin

from . import models


@admin.register(models.File)
class FileAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "name",
        "file",
        "created_at",
        "size",
        "format",
        "uuid",
    ]
