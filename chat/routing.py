from django.urls import path
from .views import helloAPI
from . import consumers

websocket_urlpatterns = [
    path('chat/<str:room_name>/<str:user_code>', consumers.ChatConsumer.as_asgi()),
    #  path('chat/<str:room_name>', consumers.ChatConsumer.as_asgi()),
]
urlpatterns = [  path("hello/",helloAPI),]