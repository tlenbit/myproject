from django.db import models, migrations
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

class Activity(models.Model):
    VOTE_UP = 'U'
    VOTE_DOWN = 'D'

    ACTIVITY_TYPES = (
        (VOTE_UP, 'Vote up'),
        (VOTE_DOWN, 'Vote down'),
    )

    user = models.ForeignKey(User)
    activity_type = models.CharField(max_length=1, choices=ACTIVITY_TYPES)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()

    class Meta:
        db_table = 'activity'
        unique_together = ['content_type', 'object_id', 'user']

class Track(models.Model):
    title = models.CharField(max_length=256)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'track'

class Artist(models.Model):
    name = models.CharField(max_length=256)
    track = models.ManyToManyField(Track)
    def __str__(self):
        return self.name

    class Meta:
        db_table = 'artist'

class Room(models.Model):
    name = models.CharField(max_length=256, unique=True)
    playlist_tracks = models.ManyToManyField(
        Track, through='Playlist_entry')
    users = models.ManyToManyField(User)
    playing_entry = models.OneToOneField(
        'Playlist_entry', 
        on_delete=models.SET_NULL, 
        related_name='+',
        null=True
    )

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'room'

class Playlist_entry(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    track = models.ForeignKey(Track, on_delete=models.CASCADE)
    # user who suggested the track
    user = models.ManyToManyField(User)
    votes = GenericRelation(Activity)

    @property
    def rating(self):
        ups = self.votes.filter(activity_type='U').count()
        downs = self.votes.filter(activity_type='D').count()
        return ups - downs

    #def __str__(self):
    #    return track.title

    class Meta:
        db_table = 'playlist_entry'

