from rest_framework import serializers
from .models import User
from dj_rest_auth.registration.serializers import RegisterSerializer

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