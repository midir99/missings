from rest_framework import serializers

from . import models


class MissingPersonPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.MissingPersonPost
        fields = "__all__"
        read_only_fields = [
            "slug",
        ]
