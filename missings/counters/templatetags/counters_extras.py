from django import template
from django.core import cache
from django.db import models as db_models

from .. import choices, models

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
    MX-MOR becomes Morelos.
    """
    return choices.StateChoices(state).label


@register.filter(is_safe=True)
def abbrstate(state):
    """
    Converts a state in ISO code to a its abbreviated representation. For example,
    MX-MOR becomes mor.
    """
    return choices.StateChoices(state).abbr()


@register.filter(is_safe=True)
def humanalert(alert):
    """
    Converts an alert to a friendly representation. For example,
    AL becomes Alba.
    """
    return choices.AlertTypeChoices(alert).label


@register.inclusion_tag("counters/components/pagination.html")
def show_pagination(paginator, page_obj, query_dict=None, page_kwarg="page"):
    ctx = {
        "page_obj": page_obj,
        "page_range": paginator.get_elided_page_range(page_obj.number),
        "pagination_required": paginator.count > 100,
        "paginator": paginator,
    }
    if query_dict is not None:
        qd = query_dict
        if page_kwarg in query_dict:
            qd = query_dict.copy()
            qd.pop(page_kwarg)

        query_string = qd.urlencode()
        ctx["query_string"] = f"&{query_string}" if query_string else ""

    return ctx


def get_six_states_with_most_missing_people():
    return models.MissingPersonPoster.objects.states_with_most_missing_people()[:6]


def get_six_states_with_less_missing_people():
    return models.MissingPersonPoster.objects.states_with_less_missing_people()[:6]


def get_state_counters_urls():
    return tuple(
        map(
            lambda s: (s.abbr(), s.label),
            choices.StateChoices,
        )
    )


@register.inclusion_tag("counters/components/links_and_stats.html")
def links_and_stats():
    cache_timeout = 60 * 15
    states_with_most_missing_people = cache.cache.get_or_set(
        "links_and_stats:states_with_most_missing_people",
        get_six_states_with_most_missing_people,
        timeout=cache_timeout,
    )
    states_with_less_missing_people = cache.cache.get_or_set(
        "links_and_stats:states_with_less_missing_people",
        get_six_states_with_less_missing_people,
        timeout=cache_timeout,
    )
    state_counters_urls = cache.cache.get_or_set(
        "links_and_stats:state_counter_urls",
        get_state_counters_urls,
        timeout=None,
    )
    return {
        "states_with_most_missing_people": states_with_most_missing_people,
        "states_with_less_missing_people": states_with_less_missing_people,
        "state_counter_urls": state_counters_urls,
    }
