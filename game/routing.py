from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('game/<str:room_name>', consumers.GameConsumer.as_asgi()),
]