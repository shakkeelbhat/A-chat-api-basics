# Import the ProtocolTypeRouter and URLRouter classes
from channels.routing import ProtocolTypeRouter, URLRouter
# Import the websocket_urlpatterns list
from chatapp.routing import websocket_urlpatterns
# Import the authentication middleware
from chatapp.middleware import TokenAuthMiddleware

# Define an ASGI application
application = ProtocolTypeRouter({
    # Map the 'websocket' protocol to the URLRouter with the authentication middleware
    'websocket': TokenAuthMiddleware(
        URLRouter(websocket_urlpatterns)
    ),
})
