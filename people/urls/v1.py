from django.urls import re_path
from .. import views

app_name = "people"
urlpatterns = [
    re_path(r"^people/", views.PeopleView.as_create()),
]
