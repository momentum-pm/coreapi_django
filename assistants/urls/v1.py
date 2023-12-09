from django.urls import re_path
from .. import views

app_name = "people"
urlpatterns = [
    re_path(
        r"^threads/$",
        views.ThreadsView.as_create(),
    ),
    re_path(
        r"^threads/(?P<thread_pk>[0-9]+)/messages/$",
        views.MessagesView.as_paginate(),
    ),
    re_path(
        r"^messages/$",
        views.MessagesView.as_create(),
    ),
]
