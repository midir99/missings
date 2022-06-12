from django.db import models
from django.db.models import functions


class MissingPersonPosterManager(models.Manager):
    """Custom manager for MissingPersonPoster entities."""

    def filter_by_loss_date(
        self, po_state=None, pub_date=None, date_from=None, date_to=None
    ):
        """Returns filtered QuerySet.

        If po_state is passed, the queryset is filtered by po_state.
        If pub_date is passed, the queryset is filtered by po_post_publication_date, and
        the date_from and date_to filters are not applied.
        If date_from or date_to are passed, the queryset is filtered by date_from and/or
        date_to (depending on which are present).
        """
        qs = self.get_queryset().annotate(
            loss_date=functions.Coalesce("missing_date", "po_post_publication_date")
        )
        if po_state:
            qs = qs.filter(po_state=po_state)
        else:
            qs = qs.all()
        if pub_date:
            qs = qs.filter(loss_date=pub_date)
        elif date_from or date_to:
            if date_from:
                qs = qs.filter(loss_date__gte=date_from)
            if date_to:
                qs = qs.filter(loss_date__lte=date_to)
        return qs

    def latest_by_loss_date(self, po_state=None):
        qs = self.get_queryset().annotate(
            loss_date=functions.Coalesce("missing_date", "po_post_publication_date")
        )
        if po_state:
            qs = qs.filter(po_state=po_state)
        else:
            qs = qs.all()
        return qs.order_by("-loss_date")

    def states_with_most_missing_people(self):
        return (
            self.get_queryset()
            .values_list(
                "po_state",
            )
            .annotate(po_state_count=models.Count("po_state"))
            .order_by("-po_state_count")
        )

    def states_with_less_missing_people(self):
        return (
            self.get_queryset()
            .values_list(
                "po_state",
            )
            .annotate(po_state_count=models.Count("po_state"))
            .order_by("po_state_count")
        )


class CounterManager(models.Manager):
    """Custom manager for Counter entities."""

    def get_counter(self):
        """Returns the first counter in the database."""
        return self.get_queryset().first()

    def get_updated_at(self):
        """Returns the updated_at field of the first counter in the database."""
        counter = self.get_counter()
        if counter is None:
            return None
        return counter.updated_at
