from django.shortcuts import render
from .models import Category
from .serializers import CategorySerializer
from django.http import JsonResponse
from django.db.models import Q
from rest_framework.decorators import api_view, permission_classes, authentication_classes
# Create your views here.

@api_view(['GET'])
@permission_classes([])
@authentication_classes([])
def category_list(request):
    category = Category.objects.all()
    serializer = CategorySerializer(category, many=True)
    return JsonResponse(serializer.data, safe=False)

@api_view(['GET'])
@permission_classes([])
@authentication_classes([])
def search_category(request):
    query = request.GET.get('query')
    category = Category.objects.filter(Q(name__icontains=query))
    serializer = CategorySerializer(category, many=True)
    return JsonResponse(serializer.data, safe=False)

# send related categories to the sector

@api_view(['GET'])
@permission_classes([])
@authentication_classes([])
def related_categories(request, sector):
    category = Category.objects.filter(sector=sector)
    serializer = CategorySerializer(category, many=True)
    return JsonResponse(serializer.data, safe=False)

