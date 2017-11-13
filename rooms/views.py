from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm

from myproject.views import login, register, logout
from rooms.models import *
from rooms.forms import UserLoginForm

import random


def index(request):
    if not request.user.is_authenticated:
        login_form = UserLoginForm()
        register_form = UserCreationForm()
        context = {
            'login_form': login_form,
            'register_form': register_form
        }
        return render(request, 'myproject/register_or_login.html', context)
    else:
        # ask room name

    '''
        if not request.session.get('guest_name', None):
            guest_name = 'stranger'+str(random.randint(1000,9999))
            request.session['guest_name'] = guest_name
        return HttpResponse('hello, '+request.session['guest_name'])
    else:
        return HttpResponse('hello, '+request.user.username)
    '''
    #return HttpResponse('if logged in: choose the room, if not: go to login page')

@login_required
def new_room(request):
    request.session['test_key'] = 'ololol'
    #return HttpResponse('(Only logged in users are allowed) Enter room name, ')
    return HttpResponse(request.user.is_authenticated)

def room(request, room_name):
    room = get_object_or_404(Room, name=room_name)
    playlist_entries_list = Playlist_entry.objects.filter(room=room)
    context = {
        'playlist_entries_list': playlist_entries_list.order_by('-rating')
    }
    return render(request, 'rooms/room.html', context)

def room_admin(request, room_name):
    return HttpResponse('Admin panel of room %s: ' % room_name)

def rate_up(request, playlist_entry_id):
    #TODO: check that a user and playlist_entry exist in the room
    pass
