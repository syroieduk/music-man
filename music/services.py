def buy_album(listener, album):
    money = listener.money or 0

    if album in listener.purchased_albums.all():
        return "You already own this album."
    if money < album.price:
        return "Not enough money."

    listener.money = money - album.price
    listener.save()
    listener.purchased_albums.add(album)
    listener.purchased_songs.add(*album.song_set.all())
    return None
