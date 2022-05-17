import datetime
import functools

from django.core import exceptions
from django.utils.translation import gettext_lazy as _


def path_params_to_date(**params):
    def decorator(func):
        @functools.wraps(func)
        def inner(request, *args, **kwargs):
            for pathparam, pathparamv in kwargs.items():
                if pathparam in params:
                    try:
                        kwargs[pathparam] = datetime.datetime.strptime(
                            pathparamv, params[pathparam]
                        )
                    except ValueError:
                        raise exceptions.BadRequest(
                            _("Invalid date: %(date)s")
                            % {
                                "date": pathparamv,
                            }
                        )

            return func(request, *args, **kwargs)

        return inner

    return decorator
