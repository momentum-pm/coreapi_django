from django.urls import path, include

app_name = "v1"

urlpatterns = [
    path(
        "authentication/",
        include("authentication.urls.v1", namespace="authentication"),
    ),
    path(
        "files/",
        include("files.urls.v1", namespace="files"),
    ),
    path(
        "assistants/",
        include("assistants.urls.v1", namespace="assistants"),
    ),
    path(
        "goals/",
        include("goals.urls.v1", namespace="goals"),
    ),
]
