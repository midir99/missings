from django import apps


class CountersConfig(apps.AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "counters"
