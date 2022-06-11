import random

from django.contrib.humanize.templatetags import humanize
from django.db import models as db_models
from django.utils import decorators as utils_decorators
from django.utils.translation import gettext_lazy as _
from django.views import generic as dj_generic
from django.views.decorators import cache
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

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["state"] = choices.StateChoices.from_abbr(self.kwargs["state"])
        ctx["counter_updated_at"] = models.Counter.objects.get_updated_at()
        ctx["mpp_count"] = models.MissingPersonPoster.objects.filter_by_loss_date(
            po_state=ctx["state"],
        ).count()
        ctx[
            "lastest_mpp_lists"
        ] = models.MissingPersonPoster.objects.latest_by_loss_date(
            po_state=ctx["state"],
        ).values(
            "mp_name",
            "circumstances_behind_dissapearance",
            "missing_from",
            "po_post_url",
            "po_poster_url",
            "loss_date",
        )[
            :6
        ]
        ctx["alba_protocol_count"] = models.MissingPersonPoster.objects.filter(
            po_state=ctx["state"],
            alert_type=choices.AlertTypeChoices.ALBA,
        ).count()
        ctx["amber_alert_count"] = models.MissingPersonPoster.objects.filter(
            po_state=ctx["state"],
            alert_type=choices.AlertTypeChoices.AMBER,
        ).count()
        ctx["odisea_alert_count"] = models.MissingPersonPoster.objects.filter(
            po_state=ctx["state"],
            alert_type=choices.AlertTypeChoices.ODISEA,
        ).count()
        ctx[
            "other_uncategorized_alert_count"
        ] = models.MissingPersonPoster.objects.filter(
            db_models.Q(alert_type=choices.AlertTypeChoices.OTHER)
            | db_models.Q(alert_type=""),
            po_state=ctx["state"],
        ).count()
        ctx["missing_female_count"] = models.MissingPersonPoster.objects.filter(
            po_state=ctx["state"],
            mp_sex=choices.SexChoices.FEMALE,
        ).count()
        ctx["missing_male_count"] = models.MissingPersonPoster.objects.filter(
            po_state=ctx["state"],
            mp_sex=choices.SexChoices.MALE,
        ).count()
        ctx["missing_other_count"] = models.MissingPersonPoster.objects.filter(
            po_state=ctx["state"],
            mp_sex="",
        ).count()
        ctx["most_common_missing_from_list"] = (
            models.MissingPersonPoster.objects.values_list(
                "missing_from",
            )
            .annotate(missing_from_count=db_models.Count("missing_from"))
            .filter(
                po_state=ctx["state"],
            )
            .order_by("-missing_from_count")[1:15]
        )
        ctx["states_with_most_missing_people"] = (
            models.MissingPersonPoster.objects.values_list(
                "po_state",
            )
            .annotate(po_state_count=db_models.Count("po_state"))
            .order_by("-po_state_count")[:5]
        )
        ctx["states_with_less_missing_people"] = (
            models.MissingPersonPoster.objects.values_list(
                "po_state",
            )
            .annotate(po_state_count=db_models.Count("po_state"))
            .order_by("po_state_count")[:6]
        )
        state_counter_urls = list(
            map(
                lambda s: (s.abbr(), s.label),
                choices.StateChoices,
            )
        )
        random.shuffle(state_counter_urls)
        ctx["state_counter_urls"] = state_counter_urls
        return ctx


counter_view = cache.cache_page(60 * 15)(CounterView.as_view())


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


about_po_websites_view = cache.cache_page(None)(AboutPOWebsitesView.as_view())
