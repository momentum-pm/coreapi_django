from django.urls import re_path
from .. import views

app_name = "people"
urlpatterns = [
    re_path(
        r"^chats/",
        views.ChatsView.as_create(),
    ),
    re_path(
        r"^messages/",
        views.MessagesView.as_create_paginate(),
    ),
]
