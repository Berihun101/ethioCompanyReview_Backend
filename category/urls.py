from django.urls import path
from . import views

urlpatterns = [
    path('category_list/', views.category_list, name='category'),
    path('search_category/', views.search_category, name='search_category'),
    path('related_categories/<str:sector>/', views.related_categories, name='related_categories'),
    
 ]