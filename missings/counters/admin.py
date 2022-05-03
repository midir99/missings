from django.contrib import admin

from . import forms, models


@admin.register(models.MissingPersonPost)
class MissingPersonPostAdmin(admin.ModelAdmin):
    model = models.MissingPersonPost
    form = forms.MissingPersonPostAdminForm
    prepopulated_fields = {
        "slug": ("mp_name",),
    }
    list_display = (
        "mp_name",
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
        "mp_name",
        "mp_sex",
        "missing_from",
        "po_state",
    ]
    ordering = [
        "-po_post_publication_date",
    ]
