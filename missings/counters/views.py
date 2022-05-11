from django.db.models import Count, Q
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, permissions
from utils import iter

from . import choices, decorators, filters, models, serializers


class MPPListCreateView(generics.ListCreateAPIView):
    """
    Use this endpoint to list and create missing person posters.
    """

    queryset = models.MissingPersonPoster.objects.all()
    serializer_class = serializers.MissingPersonPosterSerializer
    permission_classes = [
        permissions.DjangoModelPermissionsOrAnonReadOnly,
    ]
    filter_backends = [
        DjangoFilterBackend,
    ]
    filterset_class = filters.MissingPersonPosterAPIFilter


class MPPRetrieveView(generics.RetrieveAPIView):
    queryset = models.MissingPersonPoster.objects.all()
    serializer_class = serializers.MissingPersonPosterSerializer
    permission_classes = [
        permissions.AllowAny,
    ]


class TotalCounterView(TemplateView):
    template_name = "counters/total_counter.html"


class CounterView(TemplateView):
    template_name = "counters/state_counter.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["state"] = choices.StateChoices.from_abbr(self.kwargs["state"])
        ctx["mpp_count"] = models.MissingPersonPoster.objects.filter_by_loss_date(
            po_state=ctx["state"],
        ).count()
        latest_mpps_by_loss_date = (
            models.MissingPersonPoster.objects.latest_by_loss_date(
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
        )
        ctx["lastest_mpp_lists"] = iter.chunked(latest_mpps_by_loss_date, 3)
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
            Q(alert_type=choices.AlertTypeChoices.OTHER) | Q(alert_type=""),
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
            Q(mp_sex=choices.SexChoices.OTHER) | Q(mp_sex=""),
            po_state=ctx["state"],
        ).count()
        ctx["most_common_missing_from_list"] = (
            models.MissingPersonPoster.objects.values_list(
                "missing_from",
            )
            .annotate(missing_from_count=Count("missing_from"))
            .filter(
                po_state=ctx["state"],
            )
            .order_by("-missing_from_count")[1:15]
        )
        return ctx


@method_decorator(decorators.path_params_to_date(pub_date="%Y-%m-%d"), name="dispatch")
class DateCounterView(TemplateView):
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


@method_decorator(
    decorators.path_params_to_date(
        **{
            "from_": "%Y-%m-%d",
            "to": "%Y-%m-%d",
        }
    ),
    name="dispatch",
)
class DateSpanCounterView(TemplateView):
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
