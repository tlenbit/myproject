from django.db import models


class Artist(models.Model):
    name = models.CharField(max_length=256)
    
    def __str__(self):
        return self.name   


class Genre(models.Model):
    name = models.CharField(max_length=256)

    def __str__(self):
        return self.name


class Track(models.Model):
    title = models.CharField(max_length=256)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    genre = models.ManyToManyField(Genre)
    lyrics = models.CharField(max_length=16384, default='')

    def __str__(self):
        return self.title


class Room(models.Model):
    name = models.CharField(max_length=256)
    playlist_tracks = models.ManyToManyField(
        Track, through='Playlist_track')

    def __str__(self):
        return self.name


class Playlist_track(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    track = models.ForeignKey(Track, on_delete=models.CASCADE)
    votes = models.IntegerField()
