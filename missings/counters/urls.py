from django.urls import path, re_path
from django.views.decorators.cache import cache_page

from . import views

DATE_RE = r"\d{4}[-]\d{2}[-]\d{2}"
STATE_RE = (
    r"cdmx|"
    r"ags|"
    r"bc|"
    r"bcs|"
    r"camp|"
    r"coah|"
    r"col|"
    r"chis|"
    r"chih|"
    r"dgo|"
    r"gto|"
    r"gro|"
    r"hgo|"
    r"jal|"
    r"edomex|"
    r"mich|"
    r"mor|"
    r"nay|"
    r"nl|"
    r"oax|"
    r"pue|"
    r"qro|"
    r"qroo|"
    r"slp|"
    r"sin|"
    r"son|"
    r"tab|"
    r"tamps|"
    r"tlax|"
    r"ver|"
    r"yuc|"
    r"zac"
)

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
    path(
        "",
        cache_page(60 * 15)(views.TotalCounterView.as_view()),
        name="home"
    ),
    re_path(
        rf"^(?P<state>{STATE_RE})/$",
        cache_page(60 * 15)(views.CounterView.as_view()),
        name="state_counter"
    ),
    re_path(
        rf"^(?P<state>{STATE_RE})/(?P<pub_date>{DATE_RE})/$",
        cache_page(60 * 15)(views.DateCounterView.as_view()),
        name="state_date_counter",
    ),
    re_path(
        rf"^(?P<state>{STATE_RE})/(?P<from_>{DATE_RE})/(?P<to>{DATE_RE})/$",
        cache_page(60 * 15)(views.DateSpanCounterView.as_view()),
        name="state_date_span_counter",
    ),
]
