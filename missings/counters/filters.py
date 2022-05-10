from django_filters import rest_framework as filters

from . import models


class MissingPersonPosterAPIFilter(filters.FilterSet):
    name = filters.CharFilter(field_name="mp_name", lookup_expr="icontains")
    state = filters.CharFilter(field_name="po_state", lookup_expr="icontains")
    sex = filters.CharFilter(field_name="mp_sex", lookup_expr="icontains")

    class Meta:
        model = models.MissingPersonPoster
        fields = ["name", "state", "sex"]
