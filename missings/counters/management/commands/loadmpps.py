import csv
import datetime

from counters import models
from django.core.management.base import BaseCommand, CommandError
from django.utils.text import slugify


class Command(BaseCommand):
    help = "Load missing person posters into the database"

    def add_arguments(self, parser):
        parser.add_argument("csvfile", type=str)
        parser.add_argument(
            "--quotechar",
            type=str,
            default='"',
        )
        parser.add_argument("--delimiter", type=str, default=",")
        parser.add_argument(
            "--encoding",
            type=str,
            default="UTF-8",
        )
        parser.add_argument(
            "--slug-max-length",
            type=int,
            default=50,
        )

    def handle(self, *args, **options):
        with open(options["csvfile"], "rt", encoding=options["encoding"]) as csvfile:
            reader = csv.DictReader(
                csvfile,
                # [
                #     "mp_name",
                #     "po_state",
                #     "po_post_url",
                #     "po_post_publication_date",
                #     "po_poster_url",
                #     "is_multiple",
                # ],
                delimiter=options["delimiter"],
                quotechar=options["quotechar"],
            )
            mpps = tuple(reader)

        def add_slug(mpp):
            name_len = int(options["slug_max_length"] * 0.75)
            pub_date_len = int(options["slug_max_length"] * 0.25)
            mpp["slug"] = slugify(
                mpp["mp_name"][:name_len]
                + mpp["po_post_publication_date"][:pub_date_len]
            )
            return mpp

        def transform_po_post_publication_date(mpp):
            mpp["po_post_publication_date"] = datetime.datetime.strptime(
                mpp["po_post_publication_date"],
                "%Y-%m-%d",
            ).date
            return mpp

        mpps = map(add_slug, mpps)
        mpps = map(
            lambda mpp: models.MissingPersonPoster(
                mp_name=mpp["mp_name"],
                po_state=mpp["po_state"],
                po_post_url=mpp["po_post_url"],
                po_post_publication_date=mpp["po_post_publication_date"],
                po_poster_url=mpp["po_poster_url"],
                is_multiple=mpp["is_multiple"],
                slug=mpp["slug"],
            ),
            mpps,
        )
        inserted = models.MissingPersonPoster.objects.bulk_create(mpps)
        count = len(inserted)
        self.stdout.write(
            self.style.SUCCESS(
                f"{count} missing person poster(s) were inserted in the database."
            )
        )
