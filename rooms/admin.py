from django.contrib import admin

from rooms.models import Artist, Playlist_entry, Room, Track


@admin.register(Track)
class RoomsAdmin(admin.ModelAdmin):
    raw_id_fields = ('artist', )

@admin.register(Playlist_entry)
class PlaylistAdmin(admin.ModelAdmin):
    raw_id_fields = ('room', 'track', )

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    raw_id_fields = ('playlist_tracks', )

