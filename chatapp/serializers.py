from rest_framework import serializers
from .models import Message,UserProfile
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}


class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = UserProfile
        fields = ['user', 'is_online']



class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    user_profile = serializers.SerializerMethodField()
    #is_online = serializers.BooleanField()

    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')
        user = authenticate(username=username, password=password)
        if user is None:
            raise serializers.ValidationError('Invalid credentials')
        return data

    def create(self, validated_data):
        username = validated_data.get('username')
        user = User.objects.get(username=username)
        token, created = Token.objects.get_or_create(user=user)
        validated_data['token'] = token.key
        user_profile = UserProfile.objects.get(user=user)
        user_profile.is_online = True
        user_profile.save()
        return validated_data
#
    def get_user_profile(self, instance):
        user = User.objects.get(username=instance.get('username'))
        return UserProfileSerializer(user.userprofile).data
    def get_is_online(self, instance):
        # return the is_online value of the user profile
        user_profile = UserProfile.objects.get(user=instance.user)
        user_profile.is_online = True
        return user_profile.is_online

class RegisterSerializer(serializers.Serializer):
    user = UserSerializer()

    def validate(self, data):
        user_data = data.get('user')
        email = user_data.get('email')
        username = user_data.get('username')
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError('Email is already taken')
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError('Username is already taken')
        return data

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        password = user_data.pop('password')
        user = User.objects.create(**user_data)
        user.set_password(password)
        user.save()
        user_profile = UserProfile.objects.create(user=user, is_online=False)
        user_profile.save()
        return user_profile

class LogoutSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')
        user = authenticate(username=username, password=password)
        if user is None:
            raise serializers.ValidationError('Invalid credentials')
        return data


class MessageSerializer(serializers.ModelSerializer):
            class Meta:
                model = Message
                fields = ['id', 'sender', 'receiver', 'value', 'date']
