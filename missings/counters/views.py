from django.views.generic import TemplateView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, permissions

from . import choices, models, serializers


class MPPListCreateView(generics.ListCreateAPIView):
    queryset = models.MissingPersonPost.objects.all()
    serializer_class = serializers.MissingPersonPostSerializer
    permission_classes = [
        permissions.DjangoModelPermissionsOrAnonReadOnly,
    ]
    filter_backends = [
        DjangoFilterBackend,
    ]
    filterset_fields = [
        "po_state",
        "found",
        "mp_name",
    ]


class MPPRetrieveView(generics.RetrieveAPIView):
    queryset = models.MissingPersonPost.objects.all()
    serializer_class = serializers.MissingPersonPostSerializer
    permission_classes = [
        permissions.AllowAny,
    ]


class HomeView(TemplateView):
    template_name = "counters/home.html"


class CounterView(TemplateView):
    template_name = "counters/state_counter.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["state"] = choices.StateChoices.from_abbr(self.kwargs["state"])
        return ctx


class DateCounterView(TemplateView):
    pass


class DateSpanCounterView(TemplateView):
    pass
