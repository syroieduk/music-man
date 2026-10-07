from django.urls import path

from .views import (
    index,
    AlbumListView, AlbumDetailView, AlbumCreateView, AlbumUpdateView, AlbumDeleteView,
    ArtistListView, ArtistDetailView, ArtistCreateView, ArtistUpdateView, ArtistDeleteView,
    SongListView, SongDetailView, SongCreateView, SongUpdateView, SongDeleteView,
    MoodListView, MoodDetailView, MoodCreateView, MoodUpdateView, MoodDeleteView,
    ListenerListView, ListenerDetailView, ListenerCreateView, ListenerUpdateView,
    ListenerDeleteView,
    buy_album,
)

urlpatterns = [
    path("", index, name="index"),

    path("albums/", AlbumListView.as_view(), name="album-list"),
    path("albums/create/", AlbumCreateView.as_view(), name="album-create"),
    path("albums/<int:pk>/", AlbumDetailView.as_view(), name="album-detail"),
    path("albums/<int:pk>/update/", AlbumUpdateView.as_view(), name="album-update"),
    path("albums/<int:pk>/delete/", AlbumDeleteView.as_view(), name="album-delete"),
    path("albums/<int:pk>/buy/", buy_album, name="buy-album"),

    path("artists/", ArtistListView.as_view(), name="artist-list"),
    path("artists/create/", ArtistCreateView.as_view(), name="artist-create"),
    path("artists/<int:pk>/", ArtistDetailView.as_view(), name="artist-detail"),
    path("artists/<int:pk>/update/", ArtistUpdateView.as_view(), name="artist-update"),
    path("artists/<int:pk>/delete/", ArtistDeleteView.as_view(), name="artist-delete"),

    path("songs/", SongListView.as_view(), name="song-list"),
    path("songs/create/", SongCreateView.as_view(), name="song-create"),
    path("songs/<int:pk>/", SongDetailView.as_view(), name="song-detail"),
    path("songs/<int:pk>/update/", SongUpdateView.as_view(), name="song-update"),
    path("songs/<int:pk>/delete/", SongDeleteView.as_view(), name="song-delete"),

    path("moods/", MoodListView.as_view(), name="mood-list"),
    path("moods/create/", MoodCreateView.as_view(), name="mood-create"),
    path("moods/<int:pk>/", MoodDetailView.as_view(), name="mood-detail"),
    path("moods/<int:pk>/update/", MoodUpdateView.as_view(), name="mood-update"),
    path("moods/<int:pk>/delete/", MoodDeleteView.as_view(), name="mood-delete"),

    path("listeners/", ListenerListView.as_view(), name="listener-list"),
    path("listeners/create/", ListenerCreateView.as_view(), name="listener-create"),
    path("listeners/<int:pk>/", ListenerDetailView.as_view(), name="listener-detail"),
    path("listeners/<int:pk>/update/", ListenerUpdateView.as_view(), name="listener-update"),
    path("listeners/<int:pk>/delete/", ListenerDeleteView.as_view(), name="listener-delete"),
]

app_name = "music"