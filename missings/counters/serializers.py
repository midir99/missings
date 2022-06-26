from rest_framework import serializers, validators

from . import exceptions, models


class MissingPersonPosterSerializer(serializers.ModelSerializer):
    slug = serializers.SlugField(
        required=False,
        max_length=50,
        validators=[
            validators.UniqueValidator(
                queryset=models.MissingPersonPoster.objects.all()
            )
        ],
    )

    class Meta:
        model = models.MissingPersonPoster
        fields = "__all__"

    def create(self, validated_data):
        loss_date = validated_data.get("missing_date") or validated_data.get(
            "po_post_publication_date"
        )
        if not validated_data.get("slug"):
            slug = models.MissingPersonPoster.objects.find_best_slug_available(
                validated_data["mp_name"],
                loss_date=loss_date,
            )
            slug = None
            if slug is None:
                raise exceptions.UnableToGenerateSlug
            validated_data["slug"] = slug
        return super().create(validated_data)
