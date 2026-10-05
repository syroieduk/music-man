from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import Album


class AlbumForm(forms.ModelForm):
    class Meta:
        model = Album
        fields = "__all__"