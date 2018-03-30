from django.http import HttpResponse
from django.db import connection
from channels.handler import AsgiHandler
from channels import Group
from channels.auth import channel_session_user, channel_session_user_from_http

from rooms.models import Room, Track, Playlist_entry, Activity, Artist

import json
import requests
import re
import sys

# TODO: move some defs outside of this file


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
    #if processed_message.get('playlist', None).get('vote', None) is not None:
    try:
        vote(message.user,
             processed_message['playlist']['vote']['entry_id'],
             processed_message['playlist']['vote']['U_or_D']
        )
        update_info(room)
    except: 
        pass
    #if processed_message.get('chat', None) is not None:
    try:
        broadcast_chat_message(room,
                               message.user,
                               processed_message['chat']
        )
    except:
        pass
    # set next playing track
    if processed_message.get('playlist', None):
        if processed_message['playlist'].get('set_next_playing_entry', None):
            set_next_playing_entry(room)
            update_info(room)
        if processed_message['playlist'].get('add_entry'):
            add_playlist_entry(
                room,
                processed_message['playlist']['add_entry']['artist_id'],
                processed_message['playlist']['add_entry']['track_id'],
            )
            update_info(room)
    if processed_message.get('search', None):
        if processed_message['search'].get('get_artist_suggestions', None):
            artist_suggestions = suggest_artists(
                processed_message['search']['get_artist_suggestions']['partial_artist_name'],
                processed_message['search']['get_artist_suggestions']['track_choice_title']
            )
            info = {}
            info['search'] = {}
            info['search']['artist_suggestions'] = artist_suggestions
            message.reply_channel.send({"text": "%s" % json.dumps(info)})
        if processed_message.get('search').get('get_track_suggestions', None):
            track_suggestions = suggest_tracks(
                processed_message['search']['get_track_suggestions']['partial_track_title'],
                processed_message['search']['get_track_suggestions']['artist_choice_name']
            )
            info = {}
            info['search'] = {}
            info['search']['track_suggestions'] = track_suggestions
            message.reply_channel.send({"text": "%s" % json.dumps(info)})

#def print_sql_queries():
#    for query in connection.queries:
#        time = float(query['time'])
#        if time > 1:
#            print(query)

def suggest_artists(partial_artist_name, track_choice):
    RESULTS_LEN = 10
    #print_sql_queries()
    query_params = make_query_params(partial_artist_name)
    if track_choice:
        if query_params != '':
            result_query_set = Artist.objects.extra(
                where=['''to_tsvector('simple',name)@@to_tsquery('simple',%s)'''], 
                params=[query_params]
            ).filter(
                track__title=track_choice
            )[:RESULTS_LEN]
        else:
            result_query_set = Artist.objects.filter(
                track__title=track_choice
            )[:RESULTS_LEN]
    else:
        result_query_set = Artist.objects.extra(
            where=['''to_tsvector('simple',name)@@to_tsquery('simple',%s)'''], 
            params=[query_params]
        )[:RESULTS_LEN]
    return [
            { 'value': artist.id, 'label': artist.name }
            for artist in result_query_set
    ]

def make_query_params(search_string):
    # prepare query for full text search
    if search_string:
        query_params = search_string.replace(' ','&')
        if query_params[-1] != '&':
            query_params += ':*'
        else: 
            query_params = query_params[:-1]
    else:
        query_params = ''
    return query_params

def suggest_tracks(partial_track_title, artist_choice):
    RESULTS_LEN = 10
    #print_sql_queries()
    query_params = make_query_params(partial_track_title)
    if artist_choice:
        if query_params != '':
            result_query_set = Track.objects.extra(
                where=['''to_tsvector('simple',title)@@to_tsquery('simple',%s)'''], 
                params=[query_params]
            ).filter(
                artist__name=artist_choice
            )[:RESULTS_LEN]
        else:
            result_query_set = Track.objects.filter(
                artist__name=artist_choice
            )[:RESULTS_LEN]
    else:
        result_query_set = Track.objects.extra(
            where=['''to_tsvector('simple',title)@@to_tsquery('simple',%s)'''], 
            params=[query_params]
        )[:RESULTS_LEN]
    return [
            { 'value': track.id, 'label': track.title }
            for track in result_query_set
    ]

def set_next_playing_entry(room):
    if room.playing_entry:
        room.playing_entry.delete()
    top_rated_entry = get_top_rated_playlist_entry(room)
    #if top_rated_entry is not None:
    room.playing_entry = top_rated_entry
    room.save()

def add_playlist_entry(room, artist_id, track_id):
    artist = Artist.objects.get(id=artist_id)
    track = Track.objects.get(id=track_id)
    entry = Playlist_entry.objects.create(room=room, track=track)
    entry.save()
    #if room.playlist_entry_set.count() == 0:
    #    set_next_playing_entry(room)

def get_top_rated_playlist_entry(room):
    entries = Playlist_entry.objects.filter(room=room)
    if entries:
        return max(
            entries,   
            key=lambda entry: entry.rating
        )

def broadcast_chat_message(room, user, chat_message):
    info = {}
    info['chat'] = '['+user.username+'] '+chat_message
    Group(room.name).send({'text': '%s' % json.dumps(info)})

def update_info(room):
    # info on all tracks and all users in the room
    info = {
        "playlist": {},
        "users": []
    }
    if room.playing_entry is None:
        set_next_playing_entry(room)
    playing_entry = room.playing_entry
    room_playlist = list(room.playlist_entry_set.all())
    if room_playlist == []:
        return
    # TODO: fix track-artist relation
    # TODO: get url beforehand, get url for all tracks
    info['playlist']['playing_entry'] = {
        'title': playing_entry.track.title,
        'rating': playing_entry.rating,
        'artist': playing_entry.track.artist_set.all()[0].name,
        'id': playing_entry.id,
        'url': get_youtube_video_url(
            playing_entry.track.artist_set.all()[0].name +
            ' ' +
            playing_entry.track.title )
    }
    info['playlist']['entries'] = []
    for entry in room_playlist:
        info['playlist']['entries'].append({
            'title': entry.track.title,
            'rating': entry.rating,
            'artist': entry.track.artist_set.all()[0].name,
            'id': entry.id
        })
    for user in room.users.all():
        info['users'].append({'name': user.username})
    Group(room.name).send({"text": "%s" % json.dumps(info)})

def get_youtube_video_url(search_query):
    # TODO: move api key to config or smth
    search_query = re.escape(search_query).replace(' ','+').replace('&','+')
    query_url = 'https://www.googleapis.com/youtube/v3/search?'\
        'part=snippet&'\
        'q='+search_query+'&'\
        'type=video&'\
        'maxResults=1&'\
        'order=relevance&'\
        'key=AIzaSyAt3bJIrzSxR1crhuLBwXDm5qTfgm2wzBw'
    #print(query_url)
    response_data = json.loads(requests.get(query_url).text)
    #if response_data['pageInfo']['totalResults'] != 0:
    #print(response_data)
    try:
        video_id = response_data['items'][0]['id']['videoId']
        return 'https://www.youtube.com/watch?v='+video_id
    except:
        # rick roll
        return 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'

def vote(user, entry_id, U_or_D):
    entry = Playlist_entry.objects.filter(pk=entry_id).first()
    if entry is not None:
        if entry.votes.filter(user=user).exists():
            # only 1 activity object may exist due to db constraint declared in model
            vote = entry.votes.get(user=user)
            # if user have made reverse vote
            if vote.activity_type != U_or_D:
                vote.delete()
        else:
            Activity.objects.create(user=user, activity_type=U_or_D, content_object=entry).save()
