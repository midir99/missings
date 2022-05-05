from django.db import models


class MissingPersonPostManager(models.Manager):
    def filter_by_po_post_publication_date(
        self, po_state=None, publication_date=None, since=None, until=None
    ):
        """Returns filtered `QuerySet`.

        - If `po_state` is passed, the queryset is filtered by `po_state`.
        - If `publication_date` is passed, the queryset is filtered by
        `po_post_publication_date`, and the `since` and `until` filters are not applied.
        - If `since` or `until` are passed, the queryset is filtered by since and/or
        date (depending on which are present).
        """
        if po_state:
            qs = self.get_queryset().filter(po_state=po_state)
        else:
            qs = self.get_queryset().all()
        if publication_date:
            qs = qs.filter(po_post_publication_date=publication_date)
        elif since or until:
            if since:
                qs = qs.filter(po_post_publication_date__gte=since)
            if until:
                qs = qs.filter(po_post_publication_date__lte=until)
        return qs
