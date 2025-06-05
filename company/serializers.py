#import model serializers
from rest_framework import serializers
from .models import Company
from category.serializers import CategorySerializer

class CompanySerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    class Meta:
        model = Company
        fields = ['id', 'name', 'description', 'category', 'logo', 'website','email', 'phone', 'location', 'average_rating']