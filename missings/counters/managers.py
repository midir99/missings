from django.db import models
from django.db.models.functions import Coalesce


class MissingPersonPosterManager(models.Manager):
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
            loss_date=Coalesce("missing_date", "po_post_publication_date")
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
            loss_date=Coalesce("missing_date", "po_post_publication_date")
        )
        if po_state:
            qs = qs.filter(po_state=po_state)
        else:
            qs = qs.all()
        return qs.order_by("-loss_date")
