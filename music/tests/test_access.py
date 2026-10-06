from django.test import TestCase
from django.urls import reverse

from .base import create_album


class LoginRequiredTests(TestCase):
    def test_pages_redirect_anonymous_to_login(self):
        album = create_album()
        names = [
            ("music:index", []),
            ("music:album-list", []),
            ("music:album-create", []),
            ("music:album-detail", [album.pk]),
            ("music:artist-list", []),
            ("music:song-list", []),
            ("music:mood-list", []),
            ("music:listener-list", []),
        ]
        for name, args in names:
            with self.subTest(url=name):
                response = self.client.get(reverse(name, args=args))
                self.assertEqual(response.status_code, 302)
                self.assertTrue(response.url.startswith(reverse("login")))

    def test_buy_requires_login(self):
        album = create_album()
        response = self.client.post(reverse("music:buy-album", args=[album.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith(reverse("login")))

    def test_listener_create_is_open_for_anonymous(self):
        response = self.client.get(reverse("music:listener-create"))
        self.assertEqual(response.status_code, 200)
