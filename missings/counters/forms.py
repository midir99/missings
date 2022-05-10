from django import forms

from . import models


class MissingPersonPosterAdminForm(forms.ModelForm):
    class Meta:
        model = models.MissingPersonPoster
        fields = "__all__"
        widgets = {
            "mp_eyes_description": forms.Textarea,
            "mp_hair_description": forms.Textarea,
            "mp_outfit_description": forms.Textarea,
            "mp_identifying_characteristics": forms.Textarea,
            "circumstances_behind_dissapearance": forms.Textarea,
        }
