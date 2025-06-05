# import model serializers
from rest_framework import serializers

from .models import Category

# Create a serializer class
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'