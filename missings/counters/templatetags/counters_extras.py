from django import template
from django.templatetags.static import static

register = template.Library()


@register.filter(is_safe=True)
def humanint(number):
    """
    Convert a large integer to a friendly text representation. For example,
    1_000 becomes 1K,
    1_000_000 becomes 1M,
    etc.
    Values up to 10^12 (Trillion) are supported.
    """
    number = float("{:.3g}".format(number))
    magnitude = 0
    while abs(number) >= 1000:
        magnitude += 1
        number /= 1000.0
    return "{}{}".format(
        "{:f}".format(number).rstrip("0").rstrip("."),
        ["", "K", "M", "B", "T"][magnitude],
    )


@register.filter(is_safe=True)
def statemap(state):
    """
    Returns the URL of the state's map image.
    """
    return static(f"svg/maps/{state}.svg")
