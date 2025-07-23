from django.shortcuts import render
from useraccount.models import User
from rest_framework import status
from django.http import JsonResponse
from .serializers import UserDetailSerializer, GoogleSocialAuthSerializer
from rest_framework.decorators import api_view
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from cloudinary.uploader import upload
from cloudinary.exceptions import Error as CloudinaryError
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
import logging


logger = logging.getLogger(__name__)




# Create your views here.
@api_view(['GET'])
@permission_classes([])
@authentication_classes([])
def userDetail(request,id):
    try:
        user = User.objects.get(id=id)
    except User.DoesNotExist:
        return JsonResponse({'message': 'The user does not exist'}, status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        user_serializer = UserDetailSerializer(user)
        return JsonResponse(user_serializer.data)

# update the user avatar
# views.py
@api_view(['PUT'])
def updateUserAvatar(request, id):
    try:
        user = User.objects.get(id=id)
    except User.DoesNotExist:
        return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'PUT':
        if 'image' in request.FILES:
            try:
                # Upload to Cloudinary
                result = upload(
                    request.FILES['image'],
                    folder="user_avatars",
                    public_id=f"user_{user.id}",
                    overwrite=True
                )
                # Save the Cloudinary URL
                user.avatar = result['secure_url']
                user.save()
                serializer = UserDetailSerializer(user)
                return Response(serializer.data)
            except CloudinaryError as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'error': 'No image provided'}, status=status.HTTP_400_BAD_REQUEST)

# update username
@api_view(['PUT'])
def updateUsername(request, id):
    try:
        user = User.objects.get(id=id)
    except User.DoesNotExist:
        return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'PUT':
        new_username = request.data.get('username')
        if new_username:
            user.username = new_username
            user.save()
            serializer = UserDetailSerializer(user)
            return Response(serializer.data)
        return Response({'error': 'No username provided'}, status=status.HTTP_400_BAD_REQUEST)
    
class GoogleSocialAuthView(APIView):
    serializer_class = GoogleSocialAuthSerializer
    permission_classes = []  # Allow unauthenticated access

    def post(self, request):
        try:
            print("Raw request data:", request.data)  # Debug
            
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            data = serializer.validated_data
            
            print("Validated data:", data)  # Debug
            
            
            # Get or create user
            user, created = User.objects.get_or_create(
                email=data['auth_token']['email'],
                defaults={
                    'username': data['auth_token']['email'].split('@')[0],
                    'provider': data['auth_token']['provider'],
                    'social_id': data['auth_token']['social_id'],
                    'is_active': True
                }
            )
            
            # Generate tokens
            refresh = RefreshToken.for_user(user)
            return Response({
                'access': str(refresh.access_token),
                'refresh': str(refresh),
                'user_id': user.pk,
                'email': user.email
            })
            
        except Exception as e:
            print(f"View error: {str(e)}")  # Debug
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )