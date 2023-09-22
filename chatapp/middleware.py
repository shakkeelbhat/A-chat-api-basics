# Import the MiddlewareMixin class
from django.utils.deprecation import MiddlewareMixin
# Import the Token model
from rest_framework.authtoken.models import Token
# Import the AnonymousUser class
from django.contrib.auth.models import AnonymousUser


# Define a custom middleware class
class TokenAuthMiddleware(MiddlewareMixin):
    # Define the __init__ method
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.
    # Define the __call__ method
    def __call__(self, scope):
    # Code to be executed for each request before
    # the view (and later middleware) are called.
        # Get the headers from the scope
        headers = dict(scope['headers'])
        # Check if the headers contain the 'authorization' key
        if b'authorization' in headers:
            # Try to get the token from the headers
            try:
                token_name, token_key = headers[b'authorization'].decode().split()
                # Check if the token name is 'Token'
                if token_name == 'Token':
                    # Get the token object from the Token model
                    token = Token.objects.get(key=token_key)
                    # Get the user from the token
                    user = token.user
                    # Check if the user has a UserProfile model with the is_online attribute set to True
                    if user.userprofile and user.userprofile.is_online:
                        # Set the user as the scope['user']
                        scope['user'] = user
                    else:
                        # Set the scope['user'] as AnonymousUser
                        scope['user'] = AnonymousUser()
                else:
                    # Set the scope['user'] as AnonymousUser
                    scope['user'] = AnonymousUser()
            except Token.DoesNotExist:
                # Set the scope['user'] as AnonymousUser
                scope['user'] = AnonymousUser()
        else:
            # Set the scope['user'] as AnonymousUser
            scope['user'] = AnonymousUser()

        # Return the result of calling the get_response method
        return self.get_response(scope)
