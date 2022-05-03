from django.urls import path
from rest_framework.schemas import get_schema_view

from . import views

app_name = "docs"
urlpatterns = [
    path(
        "openapi/",
        get_schema_view(
            "Missings API documentation",
            description="This is the documentation for the Missings API.",
            version="0.0.0",
        ),
        name="openapi-schema",
    ),
    path("docs/", views.SwaggerUIView.as_view(), name="swagger-ui"),
]
