from django.contrib import admin

from . import forms, models


@admin.register(models.MissingPersonPoster)
class MissingPersonPosterAdmin(admin.ModelAdmin):
    model = models.MissingPersonPoster
    form = forms.MissingPersonPosterAdminForm
    prepopulated_fields = {
        "slug": ("mp_name",),
    }
    list_display = (
        "mp_name",
        "alert_type",
        "mp_dob",
        "mp_sex",
        "missing_from",
        "missing_date",
        "found",
        "po_state",
        "po_post_publication_date",
        "po_poster_url",
    )
    search_fields = [
        "id",
        "mp_name",
        "mp_sex",
        "missing_from",
        "po_state",
        "po_post_publication_date",
    ]
    ordering = [
        "-po_post_publication_date",
    ]


@admin.register(models.Counter)
class CounterAdmin(admin.ModelAdmin):
    model = models.Counter
    list_display = ("updated_at",)
