from time import time
import random

from rooms.models import Track, Artist, Room, Playlist_entry
from django.db import transaction


''' execute via ./manage.py shell < name_of_this_script.py '''

start = time()
t = start

artists_query_set = Artist.objects.all()
tracks_query_set = Track.objects.all()
tracks_count = tracks_query_set.count()
rooms_list = []
#track_artist_list = []
playlist_entries_list = []

for i in range(0, 10000):
    rooms_list.append(Room(name='room'+str(i)))

#for i in range(0, 100000):
#    artists_list.append(Artist(name='artist'+str(i)))

#print('Created 10 000 rooms, 100 000 artists models... ' + str(time()-t) )
#t = time()

# create room, artists BEFORE using 
# foreign key to them while creating tracks and rooms

Room.objects.bulk_create(rooms_list)
#Artist.objects.bulk_create(artists_list)

#print('Created db rows for rooms, artists... ' + str(time()-t) )
#t = time()

#for i in range(0, 100000):
#    tracks_list.append(
#        Track(
#            title='track'+str(i)
#        )
#    )
    
#Track.objects.bulk_create(tracks_list)

#print('Created 100 000 models and db rows for tracks... ' + str(time()-t) )
#t = time()

#ThroughModel = Artist.track.through

# create through models to apply bulk_create on them later
#for track in tracks_list:
#    track_artist_list.append(
#        ThroughModel(track=track,artist=random.choice(artists_list)))

#ThroughModel.objects.bulk_create(track_artist_list)

#print('Created 100 000 track-artist models and db rows...' + str(time()-t) )
#t = time()
i = 1
for room in rooms_list:
    print('Room '+str(i)+' ...')
    for j in range(0, 100):
        #print('  Track '+str(j)+' ...')
        try:
            track = Track.objects.get(pk=random.randint(1, tracks_count))
        except:
            pass
        playlist_entries_list.append(
            Playlist_entry(room=room, track=track)
        )
    i += 1

Playlist_entry.objects.bulk_create(playlist_entries_list)

print('Created 1 000 000 playlist_entry models and db rows ' + str(time()-t) )

print('Time elapsed: ' + str(time()-start))
