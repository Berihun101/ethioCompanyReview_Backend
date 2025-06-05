from django.shortcuts import render
from category.models import Category
from .serializers import CompanySerializer
from django.http import JsonResponse
from .models import Company
from urllib.parse import unquote
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from review.models import Review
from django.db.models import Avg

# Create your views here.

@api_view(['GET'])
@permission_classes([])
@authentication_classes([])
def category_company(request,name):
    category = Category.objects.get(name=name)
    print(category)

    if category:
        company = Company.objects.filter(category=category)
        
        serializer = CompanySerializer(company, many=True)
        return JsonResponse(serializer.data, safe=False)
    else:
        return JsonResponse({'error': 'No company found for this category'})

@api_view(['GET']) 
@permission_classes([])
@authentication_classes([]) 
def company_detail(request, id):
    try:
        # Fetch company by ID for accurate retrieval
        company = Company.objects.get(id=id)

        serializer = CompanySerializer(company)
        return JsonResponse(serializer.data, safe=False)

    except Company.DoesNotExist:
        return JsonResponse({"error": "Company not found"}, status=404)

# sending best rated companies with the category of banks whcih has 1 category id

@api_view(['GET'])
@permission_classes([])
@authentication_classes([]) 
def get_best_rated_banks(request):
    # Fetch companies and annotate them with average ratings
    best_rated_companies = (
        Company.objects.filter(category=1)
        .annotate(avg_rating=Avg('review__rating')) 
        .order_by('-avg_rating')[:5]
    )
    serializer = CompanySerializer(best_rated_companies, many=True)
    return JsonResponse(serializer.data, safe=False)

@api_view(['GET'])
@permission_classes([])
@authentication_classes([]) 
def get_best_rated_hospitals(request):
    # Fetch companies and annotate them with average ratings
    best_rated_companies = (
        Company.objects.filter(category=3)
        .annotate(avg_rating=Avg('review__rating')) 
        .order_by('-avg_rating')[:5]
    )
    serializer = CompanySerializer(best_rated_companies, many=True)
    return JsonResponse(serializer.data, safe=False)

# send number of companies in each category

@api_view(['GET'])
@permission_classes([])
@authentication_classes([])
def count_companies(request):
    categories = Category.objects.all()
    data = []
    for category in categories:
        count = Company.objects.filter(category=category).count()
        data.append({'category': category.name, 'count': count})
    return JsonResponse(data, safe=False)

