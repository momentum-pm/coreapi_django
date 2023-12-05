from django.urls import path, include

app_name = "v1"

urlpatterns = [
    path(
        "authentication/",
        include("authentication.urls.v1", namespace="authentication"),
    ),
    path(
        "people/",
        include("people.urls.v1", namespace="people"),
    ),
    path(
        "chat/",
        include("chat.urls.v1", namespace="chat"),
    ),
    path(
        "assistant/",
        include("assistant.urls.v1", namespace="assistant"),
    ),
]
