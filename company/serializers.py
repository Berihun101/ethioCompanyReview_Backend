from rest_framework import serializers
from .models import Company
from category.serializers import CategorySerializer

class CompanySerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    logo = serializers.SerializerMethodField()  # Add this
    
    class Meta:
        model = Company
        fields = ['id', 'name', 'description', 'category', 'logo', 'website', 'email', 'phone', 'location', 'average_rating']
    
    def get_logo(self, obj):
        if obj.logo:
            # Clean the URL if it contains duplicate path segments
            url = obj.logo.url
            if 'image/upload/https://' in url:
                url = 'https://' + url.split('https://')[-1]
            return url
        return None