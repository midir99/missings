import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _

from . import choices, managers


class MissingPersonPoster(models.Model):
    """Represents a missing person's poster."""

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    slug = models.SlugField(
        _("slug"),
        unique=True,
        max_length=50,  # Cannot be less than 50 characters!
        help_text=_(
            "Please enter the slug that will identify this missing person poster."
        ),
    )
    mp_name = models.CharField(
        _("missing person's name"),
        max_length=300,
        help_text=_("Please enter the name of the missing person."),
    )
    mp_height = models.PositiveSmallIntegerField(
        _("missing person's height"),
        blank=True,
        null=True,
        help_text=_("Please enter the height in centimeters of the missing person."),
    )
    mp_weight = models.PositiveSmallIntegerField(
        _("missing person's weight"),
        blank=True,
        null=True,
        help_text=_("Please enter the weight in kilograms of the missing person."),
    )
    mp_physical_build = models.CharField(
        _("missing person's physical build"),
        choices=choices.PhysicalBuildChoices.choices,
        max_length=1,
        blank=True,
        help_text=_("Please enter the physical build of the missing person."),
    )
    mp_complexion = models.CharField(
        _("missing person's complexion"),
        choices=choices.ComplexionChoices.choices,
        max_length=2,
        blank=True,
        help_text=_(
            "Please enter the complexion of the missing person (see Von Luschan's "
            "skin color scale for more information)."
        ),
    )
    mp_sex = models.CharField(
        _("missing person's sex"),
        choices=choices.SexChoices.choices,
        max_length=1,
        blank=True,
        help_text=_("Please enter the sex of the missing person."),
    )
    mp_dob = models.DateField(
        _("missing person's date of birth"),
        blank=True,
        null=True,
        help_text=_("Please enter the date of birth of the missing person."),
    )
    mp_age_when_disappeared = models.SmallIntegerField(
        _("missing person's age when disappeared"),
        blank=True,
        null=True,
        help_text=_(
            "Please enter the age the missing person had when they disappeared."
        ),
    )
    mp_eyes_description = models.CharField(
        _("missing person's eyes description"),
        max_length=500,
        blank=True,
        help_text=_("Please enter a description of the missing person's eyes."),
    )
    mp_hair_description = models.CharField(
        _("missing person's hair description"),
        max_length=500,
        blank=True,
        help_text=_("Please enter a description of the missing person's hair."),
    )
    mp_outfit_description = models.CharField(
        _("missing person's outfit description"),
        max_length=500,
        blank=True,
        help_text=_("Please enter a description of the missings person's outfit."),
    )
    mp_identifying_characteristics = models.CharField(
        _("missing person's identifying characteristics"),
        max_length=500,
        blank=True,
        help_text=_(
            "Please enter a description of the missing person's identifying "
            "characteristics."
        ),
    )
    circumstances_behind_dissapearance = models.CharField(
        _("circumstances behind dissapearance"),
        max_length=500,
        blank=True,
        help_text=_(
            "Please enter a description of the circumstances behind dissapearance."
        ),
    )
    missing_from = models.CharField(
        _("missing from"),
        max_length=150,
        blank=True,
        help_text=_("Please enter the place where the missing person was last seen."),
    )
    missing_date = models.DateField(
        _("missing date"),
        blank=True,
        null=True,
        help_text=_("Please enter the date when the missing person was last seen on."),
    )
    found = models.BooleanField(
        _("has been found?"),
        default=False,
        help_text=_("Please enter whether the missing person has been found or not."),
    )
    alert_type = models.CharField(
        _("alert type"),
        choices=choices.AlertTypeChoices.choices,
        max_length=2,
        blank=True,
        help_text=_(
            "Please enter the alert or protocol type of this missing person poster."
        ),
    )
    po_state = models.CharField(
        _("prosecutor's office state"),
        choices=choices.StateChoices.choices,
        max_length=6,
        help_text=_("Please enter the state of the prosecutor's office."),
    )
    po_post_url = models.URLField(
        _("prosecutor's office post's URL"),
        max_length=500,
        blank=True,
        help_text=_(
            "Please enter the URL of the missing person's post located on the "
            "prosecutor's office website."
        ),
    )
    po_post_publication_date = models.DateField(
        _("prosecutor's office post's publication date"),
        blank=True,
        null=True,
        help_text=_(
            "Please enter the date when the missing person's post was published on "
            "the prosecutor's office website."
        ),
    )
    po_poster_url = models.URLField(
        _("prosecutor's office poster URL"),
        max_length=500,
        blank=True,
        help_text=_(
            "Please enter the URL of the missing person's poster located on the "
            "prosecutor's office website."
        ),
    )
    is_multiple = models.BooleanField(
        _("is more than 1 person?"),
        default=False,
        help_text=_(
            "Please enter wheter this missing person poster includes more than 1 "
            "person on it."
        ),
    )

    objects = managers.MissingPersonPosterManager()

    class Meta:
        verbose_name = _("missing person poster")
        verbose_name_plural = _("missing person posters")

    def __str__(self):
        return str(self.mp_name)


class Counter(models.Model):
    """
    Represents some data about how frequently the new missing person posters are added.
    """

    updated_at = models.DateTimeField(
        _("updated at"),
        auto_now=True,
        help_text=_("Please enter the last time this counter was updated."),
    )

    objects = managers.CounterManager()

    class Meta:
        verbose_name = _("counter")
        verbose_name_plural = _("counters")

    def __str__(self):
        return f"{self.updated_at}"
