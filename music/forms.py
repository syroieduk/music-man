from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import Album, Song, Artist, Mood, Listener


class BootstrapFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs["class"] = "form-check-input"
            elif isinstance(field.widget, forms.Select):
                field.widget.attrs["class"] = "form-select"
            else:
                field.widget.attrs["class"] = "form-control"


class AlbumForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Album
        fields = "__all__"


class NameSearchForm(BootstrapFormMixin, forms.Form):
    name = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Search by name"}),
    )


class SongForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Song
        fields = "__all__"


class ArtistForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Artist
        fields = "__all__"


class MoodForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Mood
        fields = "__all__"


class ListenerCreateForm(BootstrapFormMixin, UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Listener
        fields = ["username", "first_name", "last_name", "email", "profile_picture"]


class ListenerUpdateForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Listener
        fields = ["username", "first_name", "last_name", "email", "profile_picture"]


class ListenerSearchForm(BootstrapFormMixin, forms.Form):
    username = forms.CharField(
        max_length=150,
        required=False,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Search by username"}),
    )
