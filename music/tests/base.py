from datetime import timedelta
from decimal import Decimal

from django.test import TestCase

from ..models import Album, Artist, Listener, Song


def create_album(name="Album", price="10.00"):
    return Album.objects.create(
        name=name, full_duration=timedelta(minutes=40), price=Decimal(price)
    )


def create_artist(name="Artist"):
    return Artist.objects.create(
        name=name, country="UA", amount_of_money=Decimal("0")
    )


def create_song(album, artist, name="Song"):
    return Song.objects.create(
        name=name, duration=timedelta(minutes=3), album=album, artist=artist
    )


class BaseTestCase(TestCase):
    def setUp(self):
        self.listener = Listener.objects.create_user(
            username="john",
            password="pass12345",
            first_name="John",
            last_name="Doe",
            money=Decimal("100.00"),
        )
        self.client.force_login(self.listener)
