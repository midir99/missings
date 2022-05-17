from django import template

from .. import utils

register = template.Library()


@register.filter
def chunked(value, chunk_size):
    """Does the same as utils.chunked, but in a convenient filter."""
    return utils.chunked(value, chunk_size)
