from django import template

from .. import choices

register = template.Library()


@register.filter(is_safe=True)
def humanint(number):
    """
    Converts a large integer to a friendly text representation. For example,
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
def humanstate(state):
    """
    Converts a state in ISO code to a friendly representation. For example,
    MX-MOR becomer Morelos.
    """
    return choices.StateChoices(state).label


@register.filter(is_safe=True)
def abbrstate(state):
    """
    Converts a state in ISO code to a its abbreviated representation. For example,
    MX-MOR becomer mor.
    """
    return choices.StateChoices(state).abbr()
