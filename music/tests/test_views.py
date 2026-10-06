from decimal import Decimal

from django.urls import reverse

from ..forms import ListenerCreateForm, ListenerUpdateForm
from ..models import Album, Artist, Listener, Mood, Song
from .base import BaseTestCase, create_album, create_artist, create_song


class ListViewTests(BaseTestCase):
    def test_all_lists_and_index_open(self):
        for name in [
            "music:index", "music:album-list", "music:artist-list",
            "music:song-list", "music:mood-list", "music:listener-list",
        ]:
            with self.subTest(url=name):
                self.assertEqual(self.client.get(reverse(name)).status_code, 200)

    def test_album_search_by_name(self):
        create_album(name="Thriller")
        create_album(name="Abbey Road")

        response = self.client.get(reverse("music:album-list"), {"name": "thril"})

        names = [a.name for a in response.context["album_list"]]
        self.assertEqual(names, ["Thriller"])

    def test_listener_search_by_username(self):
        Listener.objects.create_user(
            username="alice", password="x", first_name="A", last_name="B"
        )

        response = self.client.get(reverse("music:listener-list"), {"username": "ali"})

        usernames = [u.username for u in response.context["listener_list"]]
        self.assertEqual(usernames, ["alice"])

    def test_albums_are_sorted_by_name(self):
        create_album(name="B album")
        create_album(name="A album")

        response = self.client.get(reverse("music:album-list"))

        names = [a.name for a in response.context["album_list"]]
        self.assertEqual(names, ["A album", "B album"])

    def test_index_shows_own_library_counts(self):
        album = create_album()
        self.listener.purchased_albums.add(album)

        response = self.client.get(reverse("music:index"))

        self.assertEqual(response.context["albums_count"], 1)
        self.assertEqual(response.context["songs_count"], 0)

    def test_pagination_by_five(self):
        for i in range(7):
            create_album(name=f"Album {i}")

        response = self.client.get(reverse("music:album-list"))

        self.assertTrue(response.context["is_paginated"])
        self.assertEqual(len(response.context["album_list"]), 5)


class DetailViewTests(BaseTestCase):
    def test_album_detail_shows_songs(self):
        album = create_album(name="Thriller")
        create_song(album, create_artist(), name="Beat It")

        response = self.client.get(reverse("music:album-detail", args=[album.pk]))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Beat It")

    def test_detail_pages_open(self):
        album = create_album()
        artist = create_artist()
        song = create_song(album, artist)
        mood = Mood.objects.create(name="Happy")
        for name, obj in [
            ("music:album-detail", album),
            ("music:artist-detail", artist),
            ("music:song-detail", song),
            ("music:mood-detail", mood),
            ("music:listener-detail", self.listener),
        ]:
            with self.subTest(url=name):
                response = self.client.get(reverse(name, args=[obj.pk]))
                self.assertEqual(response.status_code, 200)

    def test_missing_object_gives_404(self):
        response = self.client.get(reverse("music:album-detail", args=[9999]))
        self.assertEqual(response.status_code, 404)


class CrudTests(BaseTestCase):
    def test_create_album(self):
        response = self.client.post(reverse("music:album-create"), {
            "name": "New Album",
            "full_duration": "00:40:00",
            "price": "9.99",
        })

        self.assertRedirects(response, reverse("music:album-list"))
        self.assertTrue(Album.objects.filter(name="New Album").exists())

    def test_create_album_without_name_fails(self):
        response = self.client.post(reverse("music:album-create"), {
            "full_duration": "00:40:00",
            "price": "9.99",
        })

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Album.objects.count(), 0)

    def test_update_album(self):
        album = create_album(name="Old")

        self.client.post(reverse("music:album-update", args=[album.pk]), {
            "name": "New",
            "full_duration": "00:40:00",
            "price": "10.00",
        })

        album.refresh_from_db()
        self.assertEqual(album.name, "New")

    def test_delete_album(self):
        album = create_album()

        response = self.client.post(reverse("music:album-delete", args=[album.pk]))

        self.assertRedirects(response, reverse("music:album-list"))
        self.assertFalse(Album.objects.filter(pk=album.pk).exists())

    def test_create_artist(self):
        self.client.post(reverse("music:artist-create"), {
            "name": "Queen",
            "country": "UK",
            "amount_of_money": "1000.00",
        })
        self.assertTrue(Artist.objects.filter(name="Queen").exists())

    def test_create_song(self):
        album = create_album()
        artist = create_artist()

        self.client.post(reverse("music:song-create"), {
            "name": "Yesterday",
            "duration": "00:03:00",
            "album": album.pk,
            "artist": artist.pk,
        })

        self.assertTrue(Song.objects.filter(name="Yesterday").exists())

    def test_create_mood(self):
        response = self.client.post(reverse("music:mood-create"), {
            "name": "Happy",
            "color": "#ffcc00",
        })

        self.assertRedirects(response, reverse("music:mood-list"))
        self.assertTrue(Mood.objects.filter(name="Happy").exists())

    def test_create_listener_hashes_password(self):
        response = self.client.post(reverse("music:listener-create"), {
            "username": "newbie",
            "first_name": "New",
            "last_name": "Bee",
            "password1": "pass12345",
            "password2": "pass12345",
        })

        self.assertRedirects(response, reverse("login"))
        listener = Listener.objects.get(username="newbie")
        self.assertNotEqual(listener.password, "pass12345")
        self.assertTrue(listener.check_password("pass12345"))

    def test_new_listener_cannot_choose_money(self):
        self.client.post(reverse("music:listener-create"), {
            "username": "cheater",
            "first_name": "john",
            "last_name": "cheat",
            "money": "999999",
            "password1": "passw123456",
            "password2": "passw123456",
        })

        self.assertFalse(Listener.objects.get(username="cheater").money)

    def test_listener_update_cannot_change_money(self):
        self.client.post(reverse("music:listener-update", args=[self.listener.pk]), {
            "username": "john",
            "first_name": "Johnny",
            "last_name": "Doe",
            "money": "999999",
        })

        self.listener.refresh_from_db()
        self.assertEqual(self.listener.first_name, "Johnny")
        self.assertEqual(self.listener.money, Decimal("100.00"))

    def test_listener_forms_have_no_money_or_library_fields(self):
        for form in (ListenerCreateForm(), ListenerUpdateForm()):
            for field in ("money", "purchased_albums", "purchased_songs"):
                self.assertNotIn(field, form.fields)


class BuyAlbumViewTests(BaseTestCase):
    def test_buy_album(self):
        album = create_album(price="30.00")

        response = self.client.post(
            reverse("music:buy-album", args=[album.pk]), follow=True
        )

        self.assertRedirects(response, reverse("music:album-detail", args=[album.pk]))
        self.listener.refresh_from_db()
        self.assertEqual(self.listener.money, Decimal("70.00"))
        self.assertIn(album, self.listener.purchased_albums.all())
        self.assertContains(response, "You bought")

    def test_buy_album_not_enough_money_shows_error(self):
        album = create_album(price="500.00")

        response = self.client.post(
            reverse("music:buy-album", args=[album.pk]), follow=True
        )

        self.assertContains(response, "Not enough money.")
        self.assertEqual(self.listener.purchased_albums.count(), 0)

    def test_buy_album_get_not_allowed(self):
        album = create_album()
        response = self.client.get(reverse("music:buy-album", args=[album.pk]))
        self.assertEqual(response.status_code, 405)

    def test_buy_missing_album_gives_404(self):
        response = self.client.post(reverse("music:buy-album", args=[9999]))
        self.assertEqual(response.status_code, 404)


class SongLibraryTests(BaseTestCase):
    def test_song_comes_only_with_album(self):
        album = create_album(price="10.00")
        song = create_song(album, create_artist())
        self.assertNotIn(song, self.listener.purchased_songs.all())

        self.client.post(reverse("music:buy-album", args=[album.pk]))

        self.assertIn(song, self.listener.purchased_songs.all())

    def test_song_page_shows_library_status(self):
        album = create_album()
        song = create_song(album, create_artist())
        url = reverse("music:song-detail", args=[song.pk])

        self.assertContains(self.client.get(url), "to get this song")

        self.listener.purchased_songs.add(song)

        self.assertContains(self.client.get(url), "In your library")
