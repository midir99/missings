import functools

from django.contrib.humanize.templatetags import humanize
from django.core import cache
from django.db import models as db_models
from django.utils import decorators as utils_decorators
from django.utils.translation import gettext_lazy as _
from django.views import generic as dj_generic
from django_filters import rest_framework as rf_filters
from rest_framework import generics as rf_generics
from rest_framework import permissions as rf_permissions
from rest_framework import renderers as rf_renderers
from rest_framework import response as rf_response
from rest_framework import views as rf_views

from . import choices, decorators, filters, models, serializers


class MPPListCreateView(rf_generics.ListCreateAPIView):
    queryset = models.MissingPersonPoster.objects.all()
    serializer_class = serializers.MissingPersonPosterSerializer
    permission_classes = [
        rf_permissions.DjangoModelPermissionsOrAnonReadOnly,
    ]
    filter_backends = [
        rf_filters.DjangoFilterBackend,
    ]
    filterset_class = filters.MissingPersonPosterAPIFilter
    name = _("List or create missing person posters")
    description = _("Use this endpoint to list or create missing person posters.")


mpp_list_create_view = MPPListCreateView.as_view()


class MPPRetrieveView(rf_generics.RetrieveAPIView):
    queryset = models.MissingPersonPoster.objects.all()
    serializer_class = serializers.MissingPersonPosterSerializer
    permission_classes = [
        rf_permissions.AllowAny,
    ]
    name = _("Retrieve a single missing person poster by its ID")
    description = _("Use this endpoint to retrieve missing person posters by its ID.")


mpp_retrieve_view = MPPRetrieveView.as_view()


class RetrieveUpdateCounterUpdatedAtView(rf_views.APIView):
    queryset = models.Counter.objects.all()
    permission_classes = [
        rf_permissions.DjangoModelPermissionsOrAnonReadOnly,
    ]
    renderer_classes = [
        rf_renderers.JSONRenderer,
        rf_renderers.BrowsableAPIRenderer,
        rf_renderers.StaticHTMLRenderer,
    ]
    name = _("Retrieve or update the updated_at field of the counter")
    description = _(
        "Use this endpoint to retrieve or update the updated_at field of the counter."
    )

    def get(self, request, format=None):
        updated_at = models.Counter.objects.get_updated_at()
        if request.accepted_renderer.format == "html":
            return rf_response.Response(humanize.naturaltime(updated_at))

        return rf_response.Response({"updated_at": updated_at})

    def put(self, request, format=None):
        counter = models.Counter.objects.get_counter()
        counter.save()
        if request.accepted_renderer.format == "html":
            return rf_response.Response(humanize.naturaltime(counter.updated_at))

        return rf_response.Response({"updated_at": counter.updated_at})


retrieve_update_counter_updated_at_view = RetrieveUpdateCounterUpdatedAtView.as_view()


class TotalCounterView(dj_generic.TemplateView):
    template_name = "counters/total_counter.html"


total_counter_view = TotalCounterView.as_view()


class CounterView(dj_generic.TemplateView):
    template_name = "counters/state_counter.html"

    def get_mpp_count(self, state):
        return models.MissingPersonPoster.objects.filter(
            po_state=state,
        ).count()

    def get_latest_mpp_lists(self, state):
        return models.MissingPersonPoster.objects.latest_by_loss_date(
            po_state=state,
        ).values(
            "mp_name",
            "circumstances_behind_dissapearance",
            "missing_from",
            "found",
            "alert_type",
            "po_post_url",
            "po_poster_url",
            "loss_date",
        )[
            :6
        ]

    def get_alba_protocol_count(self, state):
        return models.MissingPersonPoster.objects.filter(
            po_state=state,
            alert_type=choices.AlertTypeChoices.ALBA,
        ).count()

    def get_amber_alert_count(self, state):
        return models.MissingPersonPoster.objects.filter(
            po_state=state,
            alert_type=choices.AlertTypeChoices.AMBER,
        ).count()

    def get_odisea_alert_count(self, state):
        return models.MissingPersonPoster.objects.filter(
            po_state=state,
            alert_type=choices.AlertTypeChoices.ODISEA,
        ).count()

    def get_has_visto_a_alert_count(self, state):
        return models.MissingPersonPoster.objects.filter(
            po_state=state,
            alert_type=choices.AlertTypeChoices.HAS_VISTO_A,
        ).count()

    def get_uncategorized_alert_count(self, state):
        return models.MissingPersonPoster.objects.filter(
            po_state=state,
            alert_type="",
        ).count()

    def get_missing_female_count(self, state):
        return models.MissingPersonPoster.objects.filter(
            po_state=state,
            mp_sex=choices.SexChoices.FEMALE,
        ).count()

    def get_missing_male_count(self, state):
        return models.MissingPersonPoster.objects.filter(
            po_state=state,
            mp_sex=choices.SexChoices.MALE,
        ).count()

    def get_missing_uncategorized_sex_count(self, state):
        return models.MissingPersonPoster.objects.filter(
            po_state=state,
            mp_sex="",
        ).count()

    def get_most_common_missing_from_list(self, state):
        return (
            models.MissingPersonPoster.objects.values_list(
                "missing_from",
            )
            .annotate(missing_from_count=db_models.Count("missing_from"))
            .filter(
                po_state=state,
            )
            .order_by("-missing_from_count")[1:15]
        )

    def get_state_with_most_missing_people(self):
        return models.MissingPersonPoster.objects.states_with_most_missing_people()[0]

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["state"] = choices.StateChoices.from_abbr(self.kwargs["state"])
        ctx["counter_updated_at"] = models.Counter.objects.get_updated_at()
        cache_timeout = 60 * 15
        ctx["mpp_count"] = cache.cache.get_or_set(
            f"CounterView:get_context_data:mpp_count:{ctx['state']}",
            functools.partial(self.get_mpp_count, ctx["state"]),
            timeout=cache_timeout,
        )
        ctx["latest_mpp_lists"] = cache.cache.get_or_set(
            f"CounterView:get_context_data:latest_mpp_lists:{ctx['state']}",
            functools.partial(self.get_latest_mpp_lists, ctx["state"]),
            timeout=cache_timeout,
        )
        ctx["alba_protocol_count"] = cache.cache.get_or_set(
            f"CounterView:get_context_data:alba_protocol_count:{ctx['state']}",
            functools.partial(self.get_alba_protocol_count, ctx["state"]),
            timeout=cache_timeout,
        )
        ctx["amber_alert_count"] = cache.cache.get_or_set(
            f"CounterView:get_context_data:amber_alert_count:{ctx['state']}",
            functools.partial(self.get_amber_alert_count, ctx["state"]),
            timeout=cache_timeout,
        )
        ctx["odisea_alert_count"] = cache.cache.get_or_set(
            f"CounterView:get_context_data:odisea_alert_count:{ctx['state']}",
            functools.partial(self.get_odisea_alert_count, ctx["state"]),
            timeout=cache_timeout,
        )
        ctx["has_visto_a_alert_count"] = cache.cache.get_or_set(
            f"CounterView:get_context_data:has_visto_a_alert_count:{ctx['state']}",
            functools.partial(self.get_has_visto_a_alert_count, ctx["state"]),
            timeout=cache_timeout,
        )
        ctx["uncategorized_alert_count"] = cache.cache.get_or_set(
            f"CounterView:get_context_data:uncategorized_alert_count:{ctx['state']}",
            functools.partial(self.get_uncategorized_alert_count, ctx["state"]),
            timeout=cache_timeout,
        )
        ctx["missing_female_count"] = cache.cache.get_or_set(
            f"CounterView:get_context_data:missing_female_count:{ctx['state']}",
            functools.partial(self.get_missing_female_count, ctx["state"]),
            timeout=cache_timeout,
        )
        ctx["missing_male_count"] = cache.cache.get_or_set(
            f"CounterView:get_context_data:missing_male_count:{ctx['state']}",
            functools.partial(self.get_missing_male_count, ctx["state"]),
            timeout=cache_timeout,
        )
        ctx["missing_uncategorized_sex_count"] = cache.cache.get_or_set(
            f"CounterView:get_context_data:missing_uncategorized_sex_count:{ctx['state']}",
            functools.partial(self.get_missing_uncategorized_sex_count, ctx["state"]),
            timeout=cache_timeout,
        )
        ctx["most_common_missing_from_list"] = cache.cache.get_or_set(
            f"CounterView:get_context_data:most_common_missing_from_list:{ctx['state']}",
            functools.partial(self.get_most_common_missing_from_list, ctx["state"]),
            timeout=cache_timeout,
        )
        ctx["state_with_most_missing_people"] = cache.cache.get_or_set(
            "CounterView:get_context_data:state_with_most_missing_people",
            self.get_state_with_most_missing_people,
            timeout=cache_timeout,
        )
        return ctx


counter_view = CounterView.as_view()


@utils_decorators.method_decorator(
    decorators.path_params_to_date(pub_date="%Y-%m-%d"),
    name="dispatch",
)
class DateCounterView(dj_generic.TemplateView):
    template_name = "counters/state_date_counter.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["state"] = choices.StateChoices.from_abbr(self.kwargs["state"])
        ctx["pub_date"] = self.kwargs["pub_date"]
        ctx["mpp_count"] = models.MissingPersonPoster.objects.filter_by_loss_date(
            po_state=ctx["state"],
            pub_date=self.kwargs["pub_date"],
        ).count()
        return ctx


date_counter_view = DateCounterView.as_view()


@utils_decorators.method_decorator(
    decorators.path_params_to_date(
        **{
            "from_": "%Y-%m-%d",
            "to": "%Y-%m-%d",
        }
    ),
    name="dispatch",
)
class DateSpanCounterView(dj_generic.TemplateView):
    template_name = "counters/state_date_span_counter.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["state"] = choices.StateChoices.from_abbr(self.kwargs["state"])
        ctx["from_"] = self.kwargs["from_"]
        ctx["to"] = self.kwargs["to"]
        mpps = models.MissingPersonPoster.objects.filter_by_loss_date(
            po_state=ctx["state"],
            date_from=self.kwargs["from_"],
            date_to=self.kwargs["to"],
        )
        ctx["mpp_count"] = mpps.count()
        ctx["mpps"] = models.MissingPersonPoster.objects.latest()
        return ctx


date_span_counter_view = DateSpanCounterView.as_view()


class MPPListView(dj_generic.ListView):
    model = models.MissingPersonPoster
    context_object_name = "mpp_list"
    paginate_by = 20
    template_name = "counters/state_missings_list.html"

    def get_queryset(self):
        state = choices.StateChoices.from_abbr(self.kwargs["state"])
        qs = models.MissingPersonPoster.objects.latest_by_loss_date(po_state=state)
        mp_name = self.request.GET.get("mp_name")
        if mp_name is not None:
            qs = qs.filter(mp_name__icontains=mp_name)
        qs = qs.values(
            "mp_name",
            "circumstances_behind_dissapearance",
            "missing_from",
            "found",
            "alert_type",
            "po_post_url",
            "po_poster_url",
            "loss_date",
        )
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["state"] = choices.StateChoices.from_abbr(self.kwargs["state"])
        return ctx


mpp_list_view = MPPListView.as_view()


class AboutPOWebsitesView(dj_generic.TemplateView):
    template_name = "counters/about_po_websites.html"


about_po_websites_view = AboutPOWebsitesView.as_view()
