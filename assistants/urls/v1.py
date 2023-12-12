from django.urls import re_path
from .. import views

app_name = "people"
urlpatterns = [
    # Threads views
    re_path(
        r"^threads/$",
        views.ThreadsView.as_create_list(),
    ),
    re_path(
        r"^assistants/$",
        views.AssistantsView.as_list(),
    ),
    re_path(
        r"^threads/(?P<thread_pk>[0-9]+)/messages/$",
        views.MessagesView.as_list(),
    ),
    re_path(
        r"^calls/(?P<pk>[0-9]+)/submit-output/$",
        views.CallsView.as_view(actions={"post":"post"}),
    ),
    re_path(
        r"^messages/$",
        views.MessagesView.as_create(),
    ),
]
