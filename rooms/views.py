from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import auth
from django.urls import reverse
from django.views.generic.list import ListView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from rooms.models import Playlist_entry, Room, User
from rooms.forms import SearchRoomForm, RoomForm

import random

# '/login' '/register' '/' - same page. is it ok?
def login(request):
    form = AuthenticationForm(data=request.POST)
    if form.is_valid():
        user = auth.authenticate(
            request, 
            username=form.cleaned_data['username'], 
            password=form.cleaned_data['password']
        )
        if user is not None:
            auth.login(request, user)
            return redirect(reverse('rooms:index'))
    else:
        context = {
            'login_form': form,
            'register_form': UserCreationForm()
        }
        return render(request, 'rooms/register_or_login.html', context)

def register(request):
     form = UserCreationForm(request.POST)
     if form.is_valid():
         user = form.save()
         auth.login(request, user)
         return redirect(reverse('rooms:index'))
     else:
         context = {
             'login_form': AuthenticationForm(),
             'register_form': form
         }
         return render(request, 'rooms/register_or_login.html', context)

def logout(request):
    auth.logout(request)
    return redirect(reverse('rooms:index'))

# TODO: ask to create room if it doesn't exist already
@login_required
def search_room(request):
    rooms_list = list(Room.objects.all())
    page = request.GET.get('page', 1)
    paginator = Paginator(rooms_list, 30)
    try:
        rooms = paginator.page(page)
    except PageNotAnInteger:
        rooms = paginator.page(1)
    except EmptyPage:
        rooms = paginator.page(paginator.num_pages)
    context = { 'rooms': rooms }

    if request.method == 'POST':
        form = SearchRoomForm(request.POST)
        if form.is_valid():
            found_rooms = Room.objects.filter(name=form.cleaned_data.get('name'))
            if found_rooms.count() != 0:
                return redirect(reverse(
                    'rooms:room', 
                    kwargs={'room_name': found_rooms[0].name}
                ))
            else:
                room_name = form.cleaned_data['name']
                error_text = 'room \"' + room_name + '\" does not exist'
                form.add_error(None, error_text)
                context['search_room_form'] = form
                return render(request, 'rooms/search_or_create_room.html', context)
    else:
        context['search_room_form'] = SearchRoomForm()
        return render(request, 'rooms/search_or_create_room.html', context)


def index(request):
    if request.user.is_authenticated:
        return search_room(request)
    else:
        context = {
            'login_form': AuthenticationForm(),
            'register_form': UserCreationForm()
        }
        return render(request, 'rooms/register_or_login.html', context)

@login_required
def new_room(request):
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
        else:
            context = { 'room_form': form }
            return render(request, 'rooms/new_room.html', context)
        return redirect(reverse(
            'rooms:room',
            kwargs={'room_name': form.cleaned_data['name']}
        ))
    else:
        form = RoomForm()
        context = { 'room_form': form }
        return render(request, 'rooms/new_room.html', context)

@login_required
def room(request, room_name):
    room = get_object_or_404(Room, name=room_name)
    playlist_entries_list = Playlist_entry.objects.filter(room=room)
    context = {
        'playlist_entries_list': playlist_entries_list,
        'room': room
    }
    return render(request, 'rooms/room.html', context)

@login_required
def room_admin(request, room_name):
    return HttpResponse('Admin panel of room %s: ' % room_name)

#class RoomsView(ListView):
#    model = Room
#    paginate_by = 10
#    context_object_name = 'rooms'
#    template_name = 'rooms/search_or_create_room.html'
