from django_filters import rest_framework

from . import models


class MissingPersonPosterAPIFilter(rest_framework.FilterSet):
    mp_name = rest_framework.CharFilter(
        field_name="mp_name",
        lookup_expr="icontains",
    )
    mp_sex = rest_framework.CharFilter(
        field_name="mp_sex",
        lookup_expr="icontains",
    )
    po_state = rest_framework.CharFilter(
        field_name="po_state",
        lookup_expr="icontains",
    )
    po_post_url = rest_framework.CharFilter(
        field_name="po_post_url",
        lookup_expr="iexact",
    )
    po_poster_url = rest_framework.CharFilter(
        field_name="po_poster_url",
        lookup_expr="iexact",
    )

    class Meta:
        model = models.MissingPersonPoster
        fields = [
            "mp_name",
            "mp_sex",
            "po_state",
            "po_post_url",
            "po_poster_url",
        ]
