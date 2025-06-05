from django.urls import path
from . import views

urlpatterns = [
    path('create/<int:company_id>/', views.createReview, name='create_review'),
    path('rating/<int:company_id>/', views.get_company_rating, name='get_company_rating'),
    path('comment/<int:review_id>/', views.create_comment, name='create_comment'),
    path('average_rating/<int:company_id>/', views.get_company_average_rating, name='get_average_rating'),
    path('review_comments/<int:company_id>/', views.get_company_review_comments, name='get_review_comments'),
    path('review_comments/<uuid:reviewer_id>/<int:company_id>/', views.get_company_review_comment, name='get_review_comment'),
    path('reviewer/<int:review_id>/', views.get_reviewer_info, name='get_reviewer_info'),
    path('reviewer_rating/<uuid:reviewer_id>/<int:company_id>/', views.get_reviewer_rating, name='get_reviewer_rating'),
    path('recent_reviews/', views.get_recent_reviews, name="get_recent_reviews"),
    path('review_count/<int:company_id>/', views.get_company_review_count, name="get_company_review_count"),
    path('get_review/<int:company_id>/', views.get_review, name="get_review"),
    path('user_review_count/<uuid:reviewer_id>/', views.get_user_review_count, name="get_user_review_count"),
    path('like_comment/<int:comment_id>/', views.like_comment, name="get_review"),
    path('get_Review_like_count/<int:comment_id>/', views.get_comment_likes_count, name="get_comment_likes_count"),
    path('search_companies/', views.search_companies, name="search_companies"),
    path('reviewer_comments/<uuid:reviewer_id>/', views.get_reviewer_comments, name="get_reviewer_comments"),
    path('user_comments/<uuid:user_id>/', views.get_user_comments, name="get_user_comments"),

    
    ]