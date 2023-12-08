from django.contrib import admin
from . import models


@admin.register(models.Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ["member_count", "members"]

    def member_count(self, obj):
        return obj.members.count()

    def members(self, obj):
        return ", ".join(obj.members.all())


@admin.register(models.Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ["role", "assistant", "person"]


@admin.register(models.Membership)
class MembershipAdmin(admin.ModelAdmin):
    list_display = ["member", "chat"]


@admin.register(models.Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ["created_at", "member", "content"]
