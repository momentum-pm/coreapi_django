from django.contrib import admin
from . import models


@admin.register(models.Goal)
class GoalAdmin(admin.ModelAdmin):
    list_display = ["name", "summary", "parent", "created_at"]


@admin.register(models.Dependency)
class DependencyAdmin(admin.ModelAdmin):
    list_display = [
        "summary",
        "source",
        "target",
    ]


@admin.register(models.Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ["name", "summary"]


@admin.register(models.Record)
class RecordAdmin(admin.ModelAdmin):
    list_display = ["summary", "property", "goal", "created_at"]


@admin.register(models.EntityType)
class EntityTypeAdmin(admin.ModelAdmin):
    list_display = ["name", "summary"]


@admin.register(models.Entity)
class EntityAdmin(admin.ModelAdmin):
    list_display = ["type", "summary"]


@admin.register(models.Effect)
class EffectAdmin(admin.ModelAdmin):
    list_display = ["summary", "goal", "entity"]
