from django_filters import rest_framework as filters

from . import models


class MissingPersonPosterAPIFilter(filters.FilterSet):
    mp_name = filters.CharFilter(field_name="mp_name", lookup_expr="icontains")
    mp_sex = filters.CharFilter(field_name="mp_sex", lookup_expr="icontains")
    po_state = filters.CharFilter(field_name="po_state", lookup_expr="icontains")
    po_post_url = filters.CharFilter(field_name="po_post_url", lookup_expr="iexact")
    po_poster_url = filters.CharFilter(field_name="po_poster_url", lookup_expr="iexact")

    class Meta:
        model = models.MissingPersonPoster
        fields = [
            "mp_name",
            "mp_sex",
            "po_state",
            "po_post_url",
            "po_poster_url",
        ]
