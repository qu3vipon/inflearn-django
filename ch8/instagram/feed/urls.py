from django.urls import path

from feed import views

urlpatterns = [
    path("posts/", views.PostView.as_view(), name="posts"),
    path("posts/<int:post_id>/", views.PostDetailView.as_view(), name="post_detail"),
    path("posts/<int:post_id>/comments", views.PostCommentView.as_view(), name="post_comments"),
    path("posts/<int:post_id>/like/", views.PostLikeView.as_view(), name="post_like"),
    path("comments/<int:comment_id>/", views.PostCommentDestroyView.as_view(), name="post_comment_destroy"),
]