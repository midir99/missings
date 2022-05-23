from django import urls
from rest_framework import urlpatterns as drfurlpatterns

from . import patterns, views

api_patterns = [
    urls.path(
        "api/v1/mpps/",
        views.mpp_list_create_view,
        name="mpp_list_create",
    ),
    urls.path(
        "api/v1/mpps/<uuid:pk>/",
        views.mpp_retrieve_view,
        name="mpp_retrieve",
    ),
    urls.path(
        "api/v1/counter/updated_at/",
        views.retrieve_update_counter_updated_at_view,
        name="retrieve_update_counter_updated_at",
    ),
]

api_patterns = drfurlpatterns.format_suffix_patterns(
    api_patterns,
    allowed=["json", "api", "html"],
)

template_patterns = [
    urls.path(
        "",
        views.total_counter_view,
        name="home",
    ),
    urls.re_path(
        rf"^(?P<state>{patterns.STATE_RE})/$",
        views.counter_view,
        name="state_counter",
    ),
    urls.re_path(
        rf"^(?P<state>{patterns.STATE_RE})/(?P<date>{patterns.DATE_RE})/$",
        views.date_counter_view,
        name="state_date_counter",
    ),
    urls.re_path(
        rf"^(?P<state>{patterns.STATE_RE})/(?P<from_>{patterns.DATE_RE})/(?P<to>{patterns.DATE_RE})/$",
        views.date_span_counter_view,
        name="state_date_span_counter",
    ),
    urls.re_path(
        rf"^(?P<state>{patterns.STATE_RE})/missings/$",
        views.mpp_list_view,
        name="mpp_list",
    ),
    urls.path(
        "about-po-websites/",
        views.about_po_websites_view,
        name="about_po_websites",
    )
]

app_name = "counters"
urlpatterns = api_patterns + template_patterns
