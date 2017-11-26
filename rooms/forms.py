from django import forms
from rooms.models import Room, Track


class SearchRoomForm(forms.Form):
    name = forms.CharField(label='room name', max_length=100)

class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['name',]

class TrackForm(forms.ModelForm):
    class Meta:
        model = Track
        fields = ['title', 'artist',]
