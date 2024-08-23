from django.urls import path
from .consumers import ChatConsumer

websocket_urlpatterns = [
    path("chat/<str:uid>/", ChatConsumer.as_asgi(), name="chat"),
]
