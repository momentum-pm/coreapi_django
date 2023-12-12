from django.contrib import admin
from . import models


@admin.register(models.Assistant)
class AssistantAdmin(admin.ModelAdmin):
    list_display = ["name", "remote_uuid"]


@admin.register(models.Thread)
class ThreadAdmin(admin.ModelAdmin):
    list_display = ["member", "remote_uuid"]


@admin.register(models.Run)
class ThreadAdmin(admin.ModelAdmin):
    list_display = ["thread", "remote_uuid"]


@admin.register(models.Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ["assistant", "person"]


@admin.register(models.Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ["created_at", "content", "remote_uuid", "is_response"]


@admin.register(models.Call)
class CallAdmin(admin.ModelAdmin):
    list_display = ["func", "arguments", "output"]
