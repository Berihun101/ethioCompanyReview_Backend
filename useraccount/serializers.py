from rest_framework import serializers
from .models import User
from dj_rest_auth.registration.serializers import RegisterSerializer
from django.contrib.auth import get_user_model
from django.conf import settings
from google.oauth2 import id_token
from google.auth.transport import requests 

User = get_user_model()

class UserDetailSerializer(serializers.ModelSerializer):
    avatar_url = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'avatar_url', 'date_joined']
    
    def get_avatar_url(self, obj):
        return obj.avatar_url()

class CustomRegisterSerializer(RegisterSerializer):
    username = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)

    def save(self, request):
        user = super().save(request)
        user.username = self.validated_data.get('username')
        user.email = self.validated_data.get('email')
        user.save()
        return user

class GoogleSocialAuthSerializer(serializers.Serializer):
    auth_token = serializers.CharField()

    def validate_auth_token(self, auth_token):
        try:
            idinfo = id_token.verify_oauth2_token(
                auth_token,
                requests.Request(),
                settings.GOOGLE_OAUTH_CLIENT_ID
            )
            
            # Return the unpacked data structure directly
            return {
                'email': idinfo['email'],
                'provider': 'google',
                'social_id': idinfo['sub'],
                'first_name': idinfo.get('given_name', ''),
                'last_name': idinfo.get('family_name', '')
            }

        except ValueError as e:
            raise serializers.ValidationError(f'Google authentication failed: {str(e)}')