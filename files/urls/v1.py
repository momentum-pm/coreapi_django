from django.urls import re_path
from files import views

app_name = "files"
urlpatterns = [
    re_path(
        r"^upload/$",
        views.FilesView.as_view(actions={"post": "upload"}),
    ),
    re_path(
        r"^(?P<uuid>[a-f0-9\-]+)/$",
        views.FilesView.as_view(actions={"get": "info", "delete": "delete"}),
    ),
]
