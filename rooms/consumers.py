from django.http import HttpResponse
from channels.handler import AsgiHandler
from channels import Group
from channels.auth import channel_session_user, channel_session_user_from_http

from rooms.models import Room, Track, Playlist_entry, Activity

import json


@channel_session_user_from_http
def ws_add(message, room_name):
    # TODO: check if room password is correct
    # TODO: update only necessary info
    room = Room.objects.get(name=room_name)
    room.users.add(message.user)
    message.reply_channel.send({"accept": True})
    Group(room.name).add(message.reply_channel)
    update_info(room)

@channel_session_user
def ws_disconnect(message, room_name):
    room = Room.objects.get(name=room_name)
    room.users.remove(message.user)
    Group(room.name).discard(message.reply_channel)
    update_info(room)

@channel_session_user
def ws_message(message, room_name):
    room = Room.objects.get(name=room_name)
    processed_message = json.loads(message.content['text'])
    # U or D - up or down
    if processed_message.get('vote_on_track', None) is not None:
        vote(room,
             message.user,
             processed_message['vote_on_track']['track_title'],
             processed_message['vote_on_track']['U_or_D']
        )
        update_info(room)
    if processed_message.get('chat_message', None) is not None:
        broadcast_chat_message(room,
                               message.user,
                               processed_message['chat_message']
        )

def broadcast_chat_message(room, user, chat_message):
    info = {}
    info['chat_message'] = '['+user.username+'] '+chat_message
    Group(room.name).send({'text': '%s' % json.dumps(info)})

def update_info(room):
    # info on all tracks and all users in the room
    info = {
        "playlist_entries": [],
        "users": []
    }
    for entry in room.playlist_entry_set.all():
        info['playlist_entries'].append({
            'title': entry.track.title, 'rating': entry.rating
        })
    for user in room.users.all():
        info['users'].append({'name': user.username})
    Group(room.name).send({"text": "%s" % json.dumps(info)})

def vote(room, user, track_title, U_or_D):
    try:
        track = Track.objects.get(title=track_title)
        entry = Playlist_entry.objects.get(room=room, track=track)
        try:
            Activity.objects.get(user=user, activity_type=U_or_D, content_object=entry)
        except:
            Activity.objects.create(user=user, activity_type=U_or_D, content_object=entry).save()
    except:
        pass
