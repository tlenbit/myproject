from django.contrib import admin

from rooms.models import Room, Track, Genre, Artist


admin.site.register(Room)
admin.site.register(Track)
admin.site.register(Genre)
admin.site.register(Artist)
