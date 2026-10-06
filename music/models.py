from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class Album(models.Model):
    name = models.CharField(max_length=255)
    full_duration = models.DurationField()
    year = models.DateField(blank=True, null=True)
    description = models.TextField(max_length=800, blank=True)
    cover = models.ImageField(
        upload_to="static/images/album_covers",
        blank=True,
        null=True,
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)
    genre = models.CharField(
        max_length=255,
        blank=True,
        null=True,
    )
    def __str__(self):
        return self.name


class Artist(models.Model):
    name = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    year_of_start = models.DateField(blank=True, null=True)
    photo = models.ImageField(
        upload_to="static/images/artist_photos",
        blank=True,
        null=True,
    )
    amount_of_money = models.DecimalField(max_digits=10, decimal_places=2)
    def __str__(self):
        return self.name


class Song(models.Model):
    name = models.CharField(max_length=255)
    duration = models.DurationField()
    album = models.ForeignKey(Album, max_length=255, on_delete=models.CASCADE)
    artist = models.ForeignKey(Artist, max_length=255, on_delete=models.CASCADE)
    genre = models.CharField(
        max_length=255,
        blank=True,
        null=True,
    )
    def __str__(self):
        return self.name


class Listener(AbstractUser):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    purchased_albums = models.ManyToManyField(
        Album,
        blank=True,
        related_name="listeners"
    )
    purchased_songs = models.ManyToManyField(
        Song,
        blank=True,
        related_name="listeners"
    )
    profile_picture = models.ImageField(
        upload_to="static/images/profile_pictures",
        blank=True,
        null=True,
    )
    money = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True
    )
    date_joined = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Mood(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(max_length=800, blank=True, null=True)
    songs = models.ManyToManyField(Song, related_name="moods", blank=True)
    color = models.CharField(max_length=7, default="#808080")
    def __str__(self):
        return self.name
