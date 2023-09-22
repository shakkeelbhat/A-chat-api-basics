from rest_framework import serializers, status
from rest_framework.authtoken.serializers import AuthTokenSerializer

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from chatapp.models import Message
from .serializers import LoginSerializer, RegisterSerializer
# Use the built-in serializer and view for user registration
register_serializer = RegisterSerializer
register = ObtainAuthToken.as_view()

# Use the built-in serializer and view for user login
login_serializer = LoginSerializer
login = ObtainAuthToken.as_view()

# Create a custom serializer and view for getting online users
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'is_online']

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def online_users(request):
    # Get the current user and the list of online users
    user = request.user
    online_users = User.objects.filter(is_online=True).exclude(id=user.id)
    # Serialize the online users and return the response
    serializer = UserSerializer(online_users, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

# Create a custom serializer and view for starting a chat
class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'sender', 'receiver', 'value', 'date']

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def start_chat(request):
    # Get the current user and the selected user
    user = request.user
    selected_user_id = request.data.get('user')
    # Validate the selected user id and check if the user is online
    try:
        selected_user = User.objects.get(id=selected_user_id, is_online=True)
    except User.DoesNotExist:
        return Response({'error': 'Invalid or offline user'}, status=status.HTTP_400_BAD_REQUEST)
    # Get the messages between the current user and the selected user
    messages = Message.objects.filter(sender__in=[user, selected_user], receiver__in=[user, selected_user]).order_by('timestamp')
    # Serialize the messages and return the response
    serializer = MessageSerializer(messages, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
