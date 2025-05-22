from django.urls import path
from rest_framework_simplejwt import views as jwt_views

from user import views

# users/
urlpatterns = [
    path("", views.UserSignUpView.as_view(), name="user_sign_up"),
    path("login/", jwt_views.TokenObtainPairView.as_view(), name="user_login"),
    path("me/", views.UserMeView.as_view(), name="user_me"),
    path("<int:user_id>/", views.UserDetailView.as_view(), name="user_detail"),
    path("<int:user_id>/follow/", views.UserFollowView.as_view(), name="user_follow"),
]
