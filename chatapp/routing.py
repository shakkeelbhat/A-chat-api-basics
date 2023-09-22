# Import the path function
from django.urls import path
# Import the consumer class
from .consumers import ChatConsumer

# Define a list of WebSocket URL patterns
websocket_urlpatterns = [
    # Map the path 'ws/chat/<room_name>/' to the ChatConsumer
    path('api/chat/send/', ChatConsumer.as_asgi()),
]
