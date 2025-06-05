from rest_framework import serializers
from company.serializers import CompanySerializer

from .models import Comment, Review

class ReviewSerializer(serializers.ModelSerializer):
    company = CompanySerializer()
    class Meta:
        model = Review
        fields = ['id', 'reviewer', 'rating', 'company']

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['title', 'body']