from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from .models import Review,  Comment, CommentLike
from company.models import Company
import json
from .serializers import ReviewSerializer, CommentSerializer
from useraccount.models import User
import traceback
from django.db.models import Q
from django.core.paginator import Paginator


@api_view(["POST"])
def createReview(request, company_id):
    if request.method == "POST":
        try:
            # Fetch the company using the ID from the URL
            company = get_object_or_404(Company, id=company_id)

            # Fetch the reviewer from the logged-in user
            reviewer = request.user

            # Parse and validate the rating from the request
            
            rating = request.data.get("rating")
            if not rating or not (1 <= int(rating) <= 5):
                return JsonResponse({"error": "Rating must be between 1 and 5."}, status=400)

            # Check if the reviewer has already reviewed this company
            if Review.objects.filter(reviewer=reviewer, company=company).exists():
                return JsonResponse({"error": "You have already reviewed this company."}, status=400)

            # Create the review
            review = Review.objects.create(
                company=company,
                reviewer=reviewer,
                rating=int(rating),
            )

            review_data = {
                "id": review.id,
                "company": review.company.name,  # Assuming `Company` model has a `name` field
                "reviewer": review.reviewer.username,  # Assuming `User` model has a `username` field
                "rating": review.rating,
                "created_at": review.created_at.isoformat(),
                "updated_at": review.updated_at.isoformat(),
            }

            return JsonResponse({"message": "Review created successfully!", "review": review_data}, status=201)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request method."}, status=405)
 
@api_view(["GET"])
def get_company_rating(request, company_id):
    company = get_object_or_404(Company, id=company_id)
    review = Review.objects.filter(company=company, reviewer=request.user).first()
    serializer = ReviewSerializer(review)
    if review:
        return JsonResponse(serializer.data, safe=False)
    return JsonResponse({"rating": 0})

@api_view(["POST"])
def create_comment(request, review_id):
    if request.method == "POST":
        try:
            # Fetch the review using the ID from the URL
            review = get_object_or_404(Review, id=review_id)

            # Parse and validate the comment data from the request
            title = request.data.get("title")
            body = request.data.get("body")
            if not title or not body:
                return JsonResponse({"error": "Title and body are required."}, status=400)

            # Create the comment
            comment = Comment.objects.create(
                review=review,
                title=title,
                body=body,
            )

            comment_data = {
                "id": comment.id,
                "review_id": comment.review.id,
                "title": comment.title,
                "body": comment.body,
                "created_at": comment.created_at.isoformat(),
                "updated_at": comment.updated_at.isoformat(),
            }

            return JsonResponse({"message": "Comment created successfully!", "comment": comment_data}, status=201)

        except Exception as e:
        
            traceback.print_exc()  # Log the full stack trace
            return JsonResponse({"error": f"An unexpected error occurred: {str(e)}"}, status=500)

    return JsonResponse({"error": "Invalid request method."}, status=405)

# sending an average rating of a company

@api_view(["GET"])
@permission_classes([])
@authentication_classes([])
def get_company_average_rating(request, company_id):
    company = get_object_or_404(Company, id=company_id)
    reviews = Review.objects.filter(company=company)
    total_rating = sum(review.rating for review in reviews)
    average_rating = total_rating / len(reviews) if reviews else 0
    return JsonResponse({"rating": average_rating})

#send all the comments of a review in a company

@api_view(["GET"])
@permission_classes([])
@authentication_classes([])
def get_company_review_comments(request, company_id):
    company = get_object_or_404(Company, id=company_id)
    
    reviews = Review.objects.filter(company=company)
    comments = Comment.objects.filter(review__in=reviews).order_by("-created_at")  # Order by latest comments
    
    # Pagination setup
    page = request.GET.get("page", 1)  # Default to page 1
    per_page = request.GET.get("per_page", 5)  # Number of comments per page
    
    paginator = Paginator(comments, per_page)
    comments_page = paginator.get_page(page)

    # Serialize paginated comments
    comment_data = [
        {
            "id": comment.id,
            "review_id": comment.review.id,
            "title": comment.title,
            "body": comment.body,
            "created_at": comment.created_at.isoformat(),
        }
        for comment in comments_page
    ]

    return JsonResponse({
        "comments": comment_data,
        "total_pages": paginator.num_pages,
        "current_page": comments_page.number,
        "has_next": comments_page.has_next(),
        "has_previous": comments_page.has_previous(),
    })

#send the reviewer info of a given review id

@api_view(["GET"])
@permission_classes([])
@authentication_classes([])
def get_reviewer_info(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    reviewer = review.reviewer
    return JsonResponse({"reviewer": reviewer.username, "id": reviewer.id, "email": reviewer.email, "avatar": reviewer.avatar.url if reviewer.avatar else None})

# sending a reviewer's rating of a company with the giver reviewer id

@api_view(["GET"])
@permission_classes([])
@authentication_classes([])
def get_reviewer_rating(request, reviewer_id, company_id):
    reviewer = get_object_or_404(User, id=reviewer_id)
    company = get_object_or_404(Company, id=company_id)
    review = Review.objects.filter(reviewer=reviewer, company=company).first()
    if review:
        return JsonResponse({"rating": review.rating})
    return JsonResponse({"rating": 0})


#send recent all the recent reviews 

@api_view(["GET"])
@permission_classes([])
@authentication_classes([])

def get_recent_reviews(request):
    recent_review = Review.objects.all().order_by('-created_at')[:10]
    serializer = ReviewSerializer(recent_review, many=True)
    return JsonResponse(serializer.data, safe=False)



#send a given specific comment of a user for a company
@api_view(["GET"])
@permission_classes([])
@authentication_classes([])
def get_company_review_comment(request,reviewer_id, company_id):
    # Ensure the company exists
    company = get_object_or_404(Company, id=company_id)
    reviewer = get_object_or_404(User, id=reviewer_id)
    
    # Get all reviews for the company
    review = Review.objects.filter(company=company,reviewer=reviewer).first()
    
    # Get all comments for the reviews
    comment = Comment.objects.filter(review=review).first()
    
    serializer = CommentSerializer(comment, many=False)
    
    
    return JsonResponse(serializer.data)

#sending number of reviews of a company

@api_view(["GET"])
@permission_classes([])
@authentication_classes([])
def get_company_review_count(request, company_id):
    company = get_object_or_404(Company, id=company_id)
    review_count = Review.objects.filter(company=company).count()
    return JsonResponse({"review_count": review_count})

# from all the reviews of a company, what percentage is the rating of 5, 4, 3, 2, 1

@api_view(["GET"])
@permission_classes([])
@authentication_classes([])
def get_review(request, company_id):
    company = get_object_or_404(Company, id=company_id)
    reviews = Review.objects.filter(company=company)
    rating_5 = reviews.filter(rating=5).count()
    rating_4 = reviews.filter(rating=4).count()
    rating_3 = reviews.filter(rating=3).count()
    rating_2 = reviews.filter(rating=2).count()
    rating_1 = reviews.filter(rating=1).count()
    total_reviews = reviews.count()
    rating_5_percentage = round((rating_5 / total_reviews) * 100, 2) if total_reviews > 0 else 0
    rating_4_percentage = round((rating_4 / total_reviews) * 100, 2) if total_reviews > 0 else 0
    rating_3_percentage = round((rating_3 / total_reviews) * 100, 2) if total_reviews > 0 else 0
    rating_2_percentage = round((rating_2 / total_reviews) * 100, 2) if total_reviews > 0 else 0
    rating_1_percentage = round((rating_1 / total_reviews) * 100, 2) if total_reviews > 0 else 0

    return JsonResponse({
        "rating_5": rating_5_percentage,
        "rating_4": rating_4_percentage,
        "rating_3": rating_3_percentage,
        "rating_2": rating_2_percentage,
        "rating_1": rating_1_percentage,
    })

#send the number of review a user has given at all

@api_view(["GET"])
@permission_classes([])
@authentication_classes([])
def get_user_review_count(request, reviewer_id):
    reviewer = get_object_or_404(User, id=reviewer_id)
    review_count = Review.objects.filter(reviewer=reviewer).count()
    return JsonResponse(review_count , safe=False)

# Like a comment

@api_view(["POST"])
def like_comment(request, comment_id):
    if request.method == "POST":
        if not request.user.is_authenticated:
            return JsonResponse({"error": "Authentication required"}, status=403)
        
        comment = get_object_or_404(Comment, id=comment_id)
        
        # Check if the user already liked this comment
        like, created = CommentLike.objects.get_or_create(user=request.user, comment=comment)
        
        if created:
            return JsonResponse({"message": "Comment liked successfully", "likes_count": comment.likes_count})
        else:
            # If the like already exists, remove it (toggle functionality)
            like.delete()
            return JsonResponse({"message": "Like removed", "likes_count": comment.likes_count})

    return JsonResponse({"error": "Invalid request method"}, status=405)

#send the number of likes of a comment

@api_view(["GET"])
@permission_classes([])
@authentication_classes([])
def get_comment_likes_count(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    likes_count = comment.likes_count
    return JsonResponse({"likes_count": likes_count})

@api_view(["GET"])
@permission_classes([])
@authentication_classes([])
def search_companies(request):
    query = request.GET.get('query', '')
    if query:
        companies = Company.objects.filter(name__istartswith=query)
        results = [{"id": c.id, "name": c.name} for c in companies]
    else:
        results = []
    return JsonResponse({"data": results})

# sending individual comments of a review with a given reviewer id

@api_view(["GET"])
def get_reviewer_comments(request, reviewer_id):
    reviewer = get_object_or_404(User, id=reviewer_id)
    reviews = Review.objects.filter(reviewer=reviewer)
    comments = Comment.objects.filter(review__in=reviews).order_by("-created_at")
    comment_data = [
        {
            "id": comment.id,
            "review_id": comment.review.id,
            "company": comment.review.company.name,
            "logo": comment.review.company.logo.url,
            "rating": comment.review.rating,
            "title": comment.title,
            "body": comment.body,
            "created_at": comment.created_at.isoformat(),
        }
        for comment in comments
    ]
    return JsonResponse(comment_data, safe=False)

# sending all the comments of a commented by a user with a given user id
@api_view(["GET"])
def get_user_comments(request, user_id):
    user = get_object_or_404(User, id=user_id)
    comments = Comment.objects.filter(review__reviewer=user).order_by("-created_at")
    comment_data = [
        {
            "id": comment.id,
            "review_id": comment.review.id,
            "company": comment.review.company.name,
            "logo": comment.review.company.logo.url,
            "rating": comment.review.rating,
            "title": comment.title,
            "body": comment.body,
            "created_at": comment.created_at.isoformat(),
        }
        for comment in comments
    ]
    return JsonResponse(comment_data, safe=False)