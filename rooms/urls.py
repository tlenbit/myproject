from django.conf.urls import url

from . import views
 

app_name = 'rooms'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^new_room/$', views.new_room, name='new_room'),
    url(r'^ajax/suggest_artist_names/$',
        views.suggest_artist_names, 
        name='suggest_artist_names'
    ),
    url(r'ajax/check_username/$',
        views.check_username,
        name='check_username'
    ),
    url(r'^(?P<room_name>[\w]+)/$', views.room, name='room'),
    url(r'^(?P<room_name>[\w]+)/admin/$', views.room_admin, name='room_admin')
]
