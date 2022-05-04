from django.views.generic import TemplateView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, permissions

from . import models, serializers


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
