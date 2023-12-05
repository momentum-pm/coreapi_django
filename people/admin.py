from django.contrib import admin
from . import models


@admin.register(models.Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ["name", "about", "user"]


@admin.register(models.Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ["name"]


@admin.register(models.Membership)
class MembershipAdmin(admin.ModelAdmin):
    list_display = ["person", "team", "position"]
