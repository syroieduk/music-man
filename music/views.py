from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views import generic
from django.views.decorators.http import require_POST
from .forms import (
    AlbumForm, NameSearchForm,
)
from .models import Album, Artist, Listener, Mood, Song


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
