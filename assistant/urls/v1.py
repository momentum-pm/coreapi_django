from django.urls import re_path
from .. import views

app_name = "assistant"
urlpatterns = [
    # goals
    re_path(
        route=r"^goals/$",
        view=views.GoalsView.as_create_list(),
    ),
    re_path(
        route=r"^goals/bulk-create/$",
        view=views.GoalsView.as_bulk_create(),
    ),
    re_path(
        route=r"^goals/(?P<pk>[0-9]+)/$",
        view=views.GoalsView.as_edit_delete_retrieve(),
    ),
    # dependency
    # properties
    # records
    # entity types
    # entities
    re_path(
        route=r"^entities/$",
        view=views.EntitiesView.as_create_list(),
    ),
    re_path(
        route=r"^entities/bulk-create/$",
        view=views.EntitiesView.as_bulk_create(),
    ),
    re_path(
        route=r"^entities/(?P<pk>[0-9]+)/$",
        view=views.EntitiesView.as_retrieve_delete(),
    ),
    # effects
    re_path(
        route=r"^effects/$",
        view=views.EffectsView.as_create_list(),
    ),
    re_path(
        route=r"^effects/bulk-create/$",
        view=views.EffectsView.as_bulk_create(),
    ),
    re_path(
        route=r"^effects/(?P<pk>[0-9]+)/$",
        view=views.EffectsView.as_retrieve_delete(),
    ),
]
