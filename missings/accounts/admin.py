from django.contrib import admin
from django.contrib.auth import admin as authadmin

from . import models


@admin.register(models.User)
class UserAdmin(authadmin.UserAdmin):
    ...
