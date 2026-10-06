from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views import generic
from django.views.decorators.http import require_POST
from . import services
from .forms import (
    AlbumForm, NameSearchForm, SongForm, ArtistForm, MoodForm, ListenerUpdateForm, ListenerCreateForm,
    ListenerSearchForm,
)
from .models import Album, Artist, Listener, Mood, Song

@login_required
def index(request):
    listener = request.user

    context = {
        "listener": listener,
        "num_albums": Album.objects.count(),
        "num_songs": Song.objects.count(),
        "num_artists": Artist.objects.count(),
        "num_moods": Mood.objects.count(),
        "albums_count": listener.purchased_albums.count(),
        "songs_count": listener.purchased_songs.count(),
    }

    return render(request, "music/index.html", context=context)


class AlbumListView(LoginRequiredMixin, generic.ListView):
    model = Album
    paginate_by = 5
    ordering = ["name"]

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


class AlbumDetailView(LoginRequiredMixin, generic.DetailView):
    model = Album
    queryset = Album.objects.prefetch_related("song_set__artist")


class AlbumCreateView(LoginRequiredMixin, generic.CreateView):
    model = Album
    form_class = AlbumForm
    success_url = reverse_lazy("music:album-list")


class AlbumUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Album
    form_class = AlbumForm
    success_url = reverse_lazy("music:album-list")


class AlbumDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Album
    success_url = reverse_lazy("music:album-list")

class SongListView(LoginRequiredMixin, generic.ListView):
    model = Song
    paginate_by = 5
    queryset = Song.objects.select_related("album", "artist").order_by("name")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search_form"] = NameSearchForm()
        return context

    def get_queryset(self):
        name = self.request.GET.get("name")

        if name:
            return self.queryset.filter(name__icontains=name)

        return self.queryset


class SongDetailView(LoginRequiredMixin, generic.DetailView):
    model = Song
    queryset = Song.objects.select_related("album", "artist")


class SongCreateView(LoginRequiredMixin, generic.CreateView):
    model = Song
    form_class = SongForm
    success_url = reverse_lazy("music:song-list")


class SongUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Song
    form_class = SongForm
    success_url = reverse_lazy("music:song-list")


class SongDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Song
    success_url = reverse_lazy("music:song-list")


class ArtistListView(LoginRequiredMixin, generic.ListView):
    model = Artist
    paginate_by = 5
    ordering = ["name"]

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


class ArtistDetailView(LoginRequiredMixin, generic.DetailView):
    model = Artist
    queryset = Artist.objects.prefetch_related("song_set__album")


class ArtistCreateView(LoginRequiredMixin, generic.CreateView):
    model = Artist
    form_class = ArtistForm
    success_url = reverse_lazy("music:artist-list")


class ArtistUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Artist
    form_class = ArtistForm
    success_url = reverse_lazy("music:artist-list")


class ArtistDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Artist
    success_url = reverse_lazy("music:artist-list")


class MoodListView(LoginRequiredMixin, generic.ListView):
    model = Mood
    paginate_by = 5
    ordering = ["name"]

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


class MoodDetailView(LoginRequiredMixin, generic.DetailView):
    model = Mood
    queryset = Mood.objects.prefetch_related("songs__artist")


class MoodCreateView(LoginRequiredMixin, generic.CreateView):
    model = Mood
    form_class = MoodForm
    success_url = reverse_lazy("music:mood-list")


class MoodUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Mood
    form_class = MoodForm
    success_url = reverse_lazy("music:mood-list")


class MoodDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Mood
    success_url = reverse_lazy("music:mood-list")


class ListenerListView(LoginRequiredMixin, generic.ListView):
    model = Listener
    paginate_by = 5
    ordering = ["username"]

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


class ListenerDetailView(LoginRequiredMixin, generic.DetailView):
    model = Listener
    queryset = Listener.objects.prefetch_related(
        "purchased_albums", "purchased_songs__artist"
    )


class ListenerCreateView(generic.CreateView):
    model = Listener
    form_class = ListenerCreateForm
    success_url = reverse_lazy("login")


class ListenerUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Listener
    form_class = ListenerUpdateForm
    success_url = reverse_lazy("music:listener-list")


class ListenerDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Listener
    success_url = reverse_lazy("music:listener-list")


@login_required
@require_POST
def buy_album(request, pk):
    album = get_object_or_404(Album, id=pk)

    error = services.buy_album(request.user, album)
    if error:
        messages.error(request, error)
    else:
        messages.success(request, f"You bought {album.name}.")

    return HttpResponseRedirect(reverse_lazy("music:album-detail", args=[pk]))
