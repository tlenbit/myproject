from time import time
import random

from rooms.models import Track, Artist, Genre, Room, Playlist_entry
from django.db import transaction


''' execute via ./manage.py shell < name_of_this_script.py '''

start = time()
t = start

Artist(name='Igoryan').save()
artist = Artist.objects.get(name='Igoryan')

genres_list = []
artists_list = []
tracks_list = []
rooms_list = []
track_genre_list = []
playlist_entries_list = []

for i in range(0,1000):
    genres_list.append(Genre(name='genre'+str(i)))

for i in range(0, 10000):
    rooms_list.append(Room(name='room'+str(i)))

for i in range(0, 100000):
    artists_list.append(Artist(name='artist'+str(i)))

print('Created 1 000 genres, 10 000 rooms, 100 000 artists models... ' + str(time()-t) )
t = time()

# create genre, room, artists BEFORE using 
# foreign key to them while creating tracks and rooms

Genre.objects.bulk_create(genres_list)
Room.objects.bulk_create(rooms_list)
Artist.objects.bulk_create(artists_list)

print('Created db rows for genres, rooms, artists... ' + str(time()-t) )
t = time()

for i in range(0, 100000):
    tracks_list.append(
        Track(
            title='track'+str(i),
            artist=random.choice(artists_list)))
    
Track.objects.bulk_create(tracks_list)

print('Created 100 000 models and db rows for tracks... ' + str(time()-t) )
t = time()

ThroughModel = Track.genres.through

# create through models to apply bulk_create on them later
for track in tracks_list:
    track_genre_list.append(
        ThroughModel(track=track,genre=random.choice(genres_list)))

ThroughModel.objects.bulk_create(track_genre_list)

print('Created 100 000 track-genre models and db rows...' + str(time()-t) )
t = time()

for room in rooms_list:
    for j in range(0, 100):
        track = random.choice(tracks_list)
        playlist_entries_list.append(
            Playlist_entry(room=room, track=track))

Playlist_entry.objects.bulk_create(playlist_entries_list)

print('Created 1 000 000 playlist_entry models and db rows ' + str(time()-t) )

print('Time elapsed: ' + str(time()-start))
