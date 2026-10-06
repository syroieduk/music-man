from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from music.models import Album, Song, Artist, Mood, Listener


@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "full_duration",
        "year",
        "price",
        "genre"
    ]
    list_filter = ["name", "year", "genre"]
    list_editable = ["year", "price", "genre", "full_duration"]


@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "duration",
        "album",
        "artist",
        "genre",
    ]
    list_filter = ["name", "album", "artist", "genre"]
    list_editable = ["album", "artist", "genre"]


@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "country",
        "year_of_start",
        "amount_of_money"
    ]
    list_filter = [
        "name",
        "country",
        "year_of_start"
    ]
    list_editable = [
        "country",
        "year_of_start"
    ]

@admin.register(Mood)
class MoodAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "color",
    ]
    list_filter = [
        "name",
        "songs",
        "color"
    ]
    list_editable = [
        "color"
    ]
@admin.register(Listener)
class ListenerAdmin(UserAdmin):
    search_fields = [
        "first_name",
        "last_name",
        "email"
    ]