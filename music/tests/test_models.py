from django.test import TestCase

from ..models import Listener, Mood
from .base import create_album, create_artist, create_song


class ModelStrTests(TestCase):
    def test_album_str(self):
        self.assertEqual(str(create_album(name="Thriller")), "Thriller")

    def test_artist_str(self):
        self.assertEqual(str(create_artist(name="Queen")), "Queen")

    def test_song_str(self):
        song = create_song(create_album(), create_artist(), name="Yesterday")
        self.assertEqual(str(song), "Yesterday")

    def test_mood_str(self):
        self.assertEqual(str(Mood.objects.create(name="Happy")), "Happy")

    def test_listener_str(self):
        listener = Listener(username="jd", first_name="John", last_name="Doe")
        self.assertEqual(str(listener), "John Doe")
