from django.urls import path
from dj_rest_auth.jwt_auth import get_refresh_view
from dj_rest_auth.registration.views import RegisterView
from dj_rest_auth.views import LoginView, LogoutView, UserDetailsView
from . import views

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('<uuid:id>/',views.userDetail , name='user'),
    path('refresh/', get_refresh_view().as_view(), name='refresh'),
    path('updateAvatar/<uuid:id>/', views.updateUserAvatar, name='update_avatar'),
]