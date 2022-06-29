from rest_framework import serializers, validators

from . import exceptions, models


class MissingPersonPosterSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.MissingPersonPoster
        fields = [
            "slug",
            "mp_name",
            "mp_height",
            "mp_weight",
            "mp_physical_build",
            "mp_complexion",
            "mp_sex",
            "mp_dob",
            "mp_age_when_disappeared",
            "mp_eyes_description",
            "mp_hair_description",
            "mp_outfit_description",
            "mp_identifying_characteristics",
            "circumstances_behind_dissapearance",
            "missing_from",
            "missing_date",
            "found",
            "alert_type",
            "po_state",
            "po_post_url",
            "po_post_publication_date",
            "po_poster_url",
            "is_multiple",
        ]
        read_only_fields = [
            "slug",
        ]

    def create(self, validated_data):
        loss_date = validated_data.get("missing_date") or validated_data.get(
            "po_post_publication_date"
        )
        slug = models.MissingPersonPoster.objects.find_best_slug_available(
            validated_data["mp_name"],
            loss_date=loss_date,
        )
        if slug is None:
            raise exceptions.UnableToGenerateSlug
        validated_data["slug"] = slug
        return super().create(validated_data)
