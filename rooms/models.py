from django.db import models
from django.contrib.auth.models import User

class Artist(models.Model):
    name = models.CharField(max_length=256)
    
    def __str__(self):
        return self.name

    class Meta:
        db_table = 'artists'


class Genre(models.Model):
    name = models.CharField(max_length=256)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'genres'


class Track(models.Model):
    title = models.CharField(max_length=256)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    genres = models.ManyToManyField(Genre)
    lyrics = models.CharField(max_length=16384, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'tracks'


class Room(models.Model):
    name = models.CharField(max_length=256)
    playlist_tracks = models.ManyToManyField(
        Track, through='Playlist_entry')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'rooms'


class Playlist_entry(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    track = models.ForeignKey(Track, on_delete=models.CASCADE)
    rating = models.IntegerField()

    class Meta:
        db_table = 'playlist_entry'
