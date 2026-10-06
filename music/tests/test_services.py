from decimal import Decimal

from .. import services
from .base import BaseTestCase, create_album, create_artist, create_song


class BuyAlbumServiceTests(BaseTestCase):
    def test_successful_purchase(self):
        album = create_album(price="30.00")
        song = create_song(album, create_artist())

        error = services.buy_album(self.listener, album)

        self.assertIsNone(error)
        self.listener.refresh_from_db()
        self.assertEqual(self.listener.money, Decimal("70.00"))
        self.assertIn(album, self.listener.purchased_albums.all())
        self.assertIn(song, self.listener.purchased_songs.all())

    def test_not_enough_money(self):
        album = create_album(price="500.00")

        error = services.buy_album(self.listener, album)

        self.assertEqual(error, "Not enough money.")
        self.listener.refresh_from_db()
        self.assertEqual(self.listener.money, Decimal("100.00"))
        self.assertEqual(self.listener.purchased_albums.count(), 0)

    def test_no_money_at_all(self):
        self.listener.money = None
        self.listener.save()

        error = services.buy_album(self.listener, create_album())

        self.assertEqual(error, "Not enough money.")

    def test_cannot_buy_twice(self):
        album = create_album(price="30.00")
        services.buy_album(self.listener, album)

        error = services.buy_album(self.listener, album)

        self.assertEqual(error, "You already own this album.")
        self.listener.refresh_from_db()
        self.assertEqual(self.listener.money, Decimal("70.00"))
