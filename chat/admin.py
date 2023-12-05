from django.contrib import admin
from . import models


@admin.register(models.Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = [
        "person",
    ]


@admin.register(models.Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ["created_at", "role", "content"]
