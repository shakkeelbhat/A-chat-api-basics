from rest_framework.response import Response
from rest_framework import status
from .serializers import RegisterSerializer, LoginSerializer,UserSerializer, LogoutSerializer
from .models import UserProfile
from rest_framework.views import APIView
from sklearn.metrics.pairwise import cosine_similarity

from rest_framework.decorators import api_view

from django.contrib.auth.models import User
from rest_framework import status
from django.contrib.auth import logout
from rest_framework import generics
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token



class LogoutView(generics.CreateAPIView):
    serializer_class = LogoutSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data.get('username')
        User = get_user_model() 
        user = User.objects.get(username=username) 

        try:
            user_profile = UserProfile.objects.get(user=user)
        except:
             return Response({'message': 'Not found'})
        user_profile.is_online = False 
        user_profile.save()
        logout(request) 
        return Response({'message': 'Logged out successfully'})



    
class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_profile = serializer.save()
        user = user_profile.user 
        token, created = Token.objects.get_or_create(user=user) 
        data = {
            'user': UserSerializer(user).data,

            'token': token.key, 
        }
        return Response(data, status=status.HTTP_201_CREATED)



class LoginView(generics.CreateAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.save()
        user = User.objects.get(username=data.get('username'))
        return Response(data, status=status.HTTP_200_OK)


class OnlineUsersView(generics.ListAPIView):

    def get_queryset(self):
        return UserProfile.objects.filter(is_online=True)
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        data = []
        for user_profile in queryset:
            user = user_profile.user 
            data.append({
                'username': user.username, # return the username
                'is_online': user_profile.is_online 
            })
        return Response(data, status=status.HTTP_200_OK)


class StartChatView(APIView):
    def post(self, request):
        sender_username = request.data.get('sender')
        recipient_username = request.data.get('recepient')
        if not sender_username and not recipient_username:
            return Response({'message': 'Expecting a sender field and a recepient field'})

        if not User.objects.filter(username=sender_username):
            return Response({'message': 'Sender username does not exist. Please register the sender user'})
       
        if not User.objects.filter(username=recipient_username):
            return Response({'message': 'Recepient username does not exist. Please register the recipient user'})
        
        sender_user = User.objects.get(username=sender_username)
        sender_profile = UserProfile.objects.get(user=sender_user)
        if sender_profile.is_online:
            recipient_user = User.objects.get(username=recipient_username)
            recipient_profile = UserProfile.objects.get(user=recipient_user)
            if recipient_profile.is_online:
                return Response({'message': 'Chat started successfully'})
            else:
                return Response({'message': 'The recipient is offline or unavailable'}, status=status.HTTP_400_BAD_REQUEST)


        else:
            return Response({'message': 'You are not logged in. Please log in first'}, status=status.HTTP_400_BAD_REQUEST)


def similarity_score(user1, user2):
    common_interests = set(user1["interests"].keys()) & set(user2["interests"].keys())
    # If there are no common interests, return 0
    if not common_interests:
        return 0
    #convert the user interests to arrays of values
    user1_interests = [user1["interests"][interest] for interest in common_interests]
    user2_interests = [user2["interests"][interest] for interest in common_interests]
    cos_sim = cosine_similarity([user1_interests], [user2_interests])[0][0]
    return cos_sim

import json

@api_view(["GET"])
def suggested_friends(request, user_id):

    with open("users.json", "r") as f:
        users = json.load(f)

    user = None
    for u in users["users"]:
        if u["id"] == user_id:
            user = u
            break
    if not user:
        return Response({"error": "User not found"})
    suggestions = []
    for u in users["users"]:
        if u["id"] != user_id:
            score = similarity_score(user, u)
            suggestions.append({'user_id':u["id"],'name': u["name"],'age':u["age"],'interests':u["interests"],'match': round(score,2)})
    suggestions.sort(key=lambda x: x['match'], reverse=True)
    suggestions = suggestions[:5]
    return Response({"suggested_friends": suggestions})
        