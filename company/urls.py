from django.urls import path

from . import views

urlpatterns = [
    path('category_company/<str:name>/', views.category_company, name='category_company'),
    path('company_detail/<int:id>/', views.company_detail, name='company_detail'),
    path('best_rated_banks/', views.get_best_rated_banks, name='get_best_rated_companies'),
    path('best_rated_hospitals/', views.get_best_rated_hospitals, name='get_best_rated_hospital'),
    path('count_companies/', views.count_companies, name='count_companies'),
   
]