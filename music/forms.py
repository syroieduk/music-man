from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import Album, Song


class AlbumForm(forms.ModelForm):
    class Meta:
        model = Album
        fields = "__all__"


class NameSearchForm(forms.Form):
    name = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Search by name"}),
    )


class SongForm(forms.ModelForm):
    class Meta:
        model = Song
        fields = "all"


