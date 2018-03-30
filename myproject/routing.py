from channels.routing import route
from rooms.consumers import ws_message, ws_add, ws_disconnect


channel_routing = [
    route('websocket.connect', ws_add, path=r'^/ws/rooms/(?P<room_name>[\w]+)/admin/$'),
    route('websocket.receive', ws_message, path=r'^/ws/rooms/(?P<room_name>[\w]+)/admin/$'),
    route('websocket.disconnect', ws_disconnect, path=r'^/ws/rooms/(?P<room_name>[\w]+)/admin/$'),
    route('websocket.connect', ws_add, path=r'^/ws/rooms/(?P<room_name>[\w]+)/$'),
    route('websocket.receive', ws_message, path=r'^/ws/rooms/(?P<room_name>[\w]+)/$'),
    route('websocket.disconnect', ws_disconnect, path=r'^/ws/rooms/(?P<room_name>[\w]+)/$'),
    ]
