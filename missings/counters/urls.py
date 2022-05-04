from django.urls import path

from . import views

app_name = "counters"
urlpatterns = [
    # API views
    path(
        "api/v1/mpps/",
        views.MPPListCreateView.as_view(),
        name="mpp-list-create",
    ),
    path(
        "api/v1/mpps/<uuid:pk>/",
        views.MPPRetrieveView.as_view(),
        name="mpp-retrieve",
    ),
    # Template views
    path("", views.HomeView.as_view(), name="home"),
]
