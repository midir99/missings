from rest_framework import serializers

from . import models


class MissingPersonPosterSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.MissingPersonPoster
        fields = "__all__"
        read_only_fields = [
            "slug",
        ]
