from django.conf import settings

from django.urls import path, include
from .setup_urls import setup

urlpatterns = []
if settings.ENV.API_VERSION == "v1":
    urlpatterns.append(
        path("v1/", include("coreapi_django.version_urls.v1", namespace="v1"))
    )
urlpatterns = setup(urlpatterns)
