from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from rooms.models import Room, Track


class CustomUserCreationForm(UserCreationForm):
    password1 = forms.CharField(
        label='',
        strip=False,
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 
                   'placeholder': 'Password'
            }
        ),
        help_text=None,
    )
    password2 = forms.CharField(
        label='',
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 
                   'placeholder': 'Password again...'
            }
        ),
        strip=False,
        help_text=None,
    )
    username = forms.CharField(
        label='',
        widget=forms.TextInput(
            attrs={'id': 'register-username-input',
                   'class': 'form-control', 
                   'placeholder': 'Username'
            }
        )
    )

class CustomAuthForm(AuthenticationForm):
    username = forms.CharField(
        label='',
        widget=forms.TextInput(
            attrs={'id': 'login-username-input', 
                   'class': 'form-control', 
                   'placeholder': 'Username'
            }
        )
    )
    password = forms.CharField(
        label='',
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 
                   'placeholder': 'Password'
            }
        )
    )

class SearchRoomForm(forms.Form):
    name = forms.CharField(
        label='', 
        max_length=100, 
        widget=forms.TextInput(
            attrs={'id': 'search-room-input', 
                   'class': 'form-control', 
                   'placeholder': 'Room name', 
                   'autofocus': True
            }
        )
    )

class RoomForm(forms.ModelForm):
    name = forms.CharField(
        label='', 
        max_length=100, 
        widget=forms.TextInput(
            attrs={
                'class': 'form-control', 
                'placeholder': 'Room name'
            }
        )
    )
    class Meta:
        model = Room
        fields = ['name',]

class TrackForm(forms.ModelForm):
    class Meta:
        model = Track
        fields = ['title', ]
