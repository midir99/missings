from rest_framework import generics, mixins, permissions

from . import models, serializers


class MPPListCreateView(generics.ListCreateAPIView):
    queryset = models.MissingPersonPost.objects.all()
    serializer_class = serializers.MissingPersonPostSerializer
    permission_classes = [
        permissions.DjangoModelPermissionsOrAnonReadOnly,
    ]


class MPPRetrieveView(generics.RetrieveAPIView):
    queryset = models.MissingPersonPost.objects.all()
    serializer_class = serializers.MissingPersonPostSerializer
    permission_classes = [
        permissions.AllowAny,
    ]
