from django.utils.translation import gettext_lazy as _
from rest_framework import exceptions as drfexceptions
from rest_framework import status as drfstatus


class UnableToGenerateSlug(drfexceptions.APIException):
    status_code = drfstatus.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = _(
        "We could not generate the slug for the missing person poster, please try "
        "again with a different slug."
    )
