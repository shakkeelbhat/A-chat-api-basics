# chatapp_project/routing.py
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from chatapp import routing

application = ProtocolTypeRouter({
    # A protocol type router for WebSocket connections
    'websocket': AuthMiddlewareStack(
        URLRouter(
            routing.websocket_urlpatterns
        )
    ),
})
