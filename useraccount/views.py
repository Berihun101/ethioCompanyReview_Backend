from django.shortcuts import render
from useraccount.models import User
from rest_framework import status
from django.http import JsonResponse
from .serializers import UserDetailSerializer
from rest_framework.decorators import api_view
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


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
        # Handle file upload from FormData
        if 'image' in request.FILES:
            user.avatar = request.FILES['image']
            user.save()
            serializer = UserDetailSerializer(user)
            return Response(serializer.data)
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