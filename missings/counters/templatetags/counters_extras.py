from django import template

register = template.Library()


@register.filter(is_safe=True)
def humanint(value):
    """
    Convert a large integer to a friendly text representation. For example,
    1_000 becomes 1K,
    1_000_000 becomes 1M,
    etc.
    Values up to 10^12 (Trillion) are supported.
    """
    value = float('{:.3g}'.format(value))
    magnitude = 0
    while abs(value) >= 1000:
        magnitude += 1
        value /= 1000.0
    return '{}{}'.format(
        '{:f}'.format(value).rstrip('0').rstrip('.'),
        ['', 'K', 'M', 'B', 'T'][magnitude],
    )
