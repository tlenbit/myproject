from django.conf.urls import url

from . import views
 

app_name = 'rooms'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(),
    url(r'^new_room/$', views.new_room, name='new_room'),
    url(r'^(?P<room_name>[\w]+)/$', views.room, name='room'),
    url(r'^(?P<room_name>[\w]+)/admin/$', views.room_admin, name='room_admin')
]
