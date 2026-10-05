from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views import generic
from django.views.decorators.http import require_POST
from .forms import (
    AlbumForm, NameSearchForm, SongForm, ArtistForm, MoodForm, ListenerUpdateForm, ListenerCreateForm,
    ListenerSearchForm,
)
from .models import Album, Artist, Listener, Mood, Song

def index(request):
    listener_id = request.GET.get("listener")
    listener = None

    if listener_id:
        listener = Listener.objects.filter(pk=listener_id).first()

    context = {
        "listeners": Listener.objects.all(),
        "listener": listener,
        "num_albums": Album.objects.count(),
        "num_songs": Song.objects.count(),
        "num_artists": Artist.objects.count(),
        "num_moods": Mood.objects.count(),
    }

    if listener:
        context["albums_count"] = listener.purchased_albums.count()
        context["songs_count"] = listener.purchased_songs.count()

    return render(request, "music/index.html", context=context)


class AlbumListView(generic.ListView):
    model = Album
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search_form"] = NameSearchForm()
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        name = self.request.GET.get("name")

        if name:
            return queryset.filter(name__icontains=name)

        return queryset


class AlbumDetailView(generic.DetailView):
    model = Album
    queryset = Album.objects.prefetch_related("song_set__artist")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["listeners"] = Listener.objects.all()
        return context


class AlbumCreateView(generic.CreateView):
    model = Album
    form_class = AlbumForm
    success_url = reverse_lazy("music:album-list")


class AlbumUpdateView(generic.UpdateView):
    model = Album
    form_class = AlbumForm
    success_url = reverse_lazy("music:album-list")


class AlbumDeleteView(generic.DeleteView):
    model = Album
    success_url = reverse_lazy("music:album-list")

class SongListView(generic.ListView):
    model = Song
    paginate_by = 5
    queryset = Song.objects.select_related("album", "artist")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search_form"] = NameSearchForm()
        return context

    def get_queryset(self):
        name = self.request.GET.get("name")

        if name:
            return self.queryset.filter(name__icontains=name)

        return self.queryset


class SongDetailView(generic.DetailView):
    model = Song
    queryset = Song.objects.select_related("album", "artist")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["listeners"] = Listener.objects.all()
        return context


class SongCreateView(generic.CreateView):
    model = Song
    form_class = SongForm
    success_url = reverse_lazy("music:song-list")


class SongUpdateView(generic.UpdateView):
    model = Song
    form_class = SongForm
    success_url = reverse_lazy("music:song-list")


class SongDeleteView(generic.DeleteView):
    model = Song
    success_url = reverse_lazy("music:song-list")


class ArtistListView(generic.ListView):
    model = Artist
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search_form"] = NameSearchForm()
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        name = self.request.GET.get("name")

        if name:
            return queryset.filter(name__icontains=name)

        return queryset


class ArtistDetailView(generic.DetailView):
    model = Artist
    queryset = Artist.objects.prefetch_related("song_set__album")


class ArtistCreateView(generic.CreateView):
    model = Artist
    form_class = ArtistForm
    success_url = reverse_lazy("music:artist-list")


class ArtistUpdateView(generic.UpdateView):
    model = Artist
    form_class = ArtistForm
    success_url = reverse_lazy("music:artist-list")


class ArtistDeleteView(generic.DeleteView):
    model = Artist
    success_url = reverse_lazy("music:artist-list")


class MoodListView(generic.ListView):
    model = Mood
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search_form"] = NameSearchForm()
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        name = self.request.GET.get("name")

        if name:
            return queryset.filter(name__icontains=name)

        return queryset


class MoodDetailView(generic.DetailView):
    model = Mood
    queryset = Mood.objects.prefetch_related("songs__artist")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["other_songs"] = Song.objects.exclude(moods=self.object)
        return context


class MoodCreateView(generic.CreateView):
    model = Mood
    form_class = MoodForm
    success_url = reverse_lazy("music:mood-list")


class MoodUpdateView(generic.UpdateView):
    model = Mood
    form_class = MoodForm
    success_url = reverse_lazy("music:mood-list")


class MoodDeleteView(generic.DeleteView):
    model = Mood
    success_url = reverse_lazy("music:mood-list")


class ListenerListView(generic.ListView):
    model = Listener
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search_form"] = ListenerSearchForm()
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        username = self.request.GET.get("username")

        if username:
            return queryset.filter(username__icontains=username)

        return queryset


class ListenerDetailView(generic.DetailView):
    model = Listener
    queryset = Listener.objects.prefetch_related(
        "purchased_albums", "purchased_songs__artist"
    )


class ListenerCreateView(generic.CreateView):
    model = Listener
    form_class = ListenerCreateForm
    success_url = reverse_lazy("music:listener-list")


class ListenerUpdateView(generic.UpdateView):
    model = Listener
    form_class = ListenerUpdateForm
    success_url = reverse_lazy("music:listener-list")


class ListenerDeleteView(generic.DeleteView):
    model = Listener
    success_url = reverse_lazy("music:listener-list")