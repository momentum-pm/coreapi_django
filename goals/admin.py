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


@admin.register(models.Metric)
class MetricAdmin(admin.ModelAdmin):
    list_display = ["name", "summary"]


@admin.register(models.MetricValue)
class MetricValueAdmin(admin.ModelAdmin):
    list_display = ["value", "metric", "goal", "created_at"]


@admin.register(models.Entity)
class EntityAdmin(admin.ModelAdmin):
    list_display = ["summary"]


@admin.register(models.Effect)
class EffectAdmin(admin.ModelAdmin):
    list_display = ["summary", "goal", "entity"]


@admin.register(models.Person)
class PersonADmin(admin.ModelAdmin):
    list_display = ["name", "about", "id"]


@admin.register(models.Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ["information", "sender", "goal", "is_seen"]


@admin.register(models.Action)
class ActionAdmin(admin.ModelAdmin):
    list_display = ["person", "goal", "summary"]
