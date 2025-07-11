# import model serializers
from rest_framework import serializers

from .models import Category

# Create a serializer class
class CategorySerializer(serializers.ModelSerializer):
    icon_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'sector', 'icon_url']
        
    def get_icon_url(self, obj):
        return obj.icon_url