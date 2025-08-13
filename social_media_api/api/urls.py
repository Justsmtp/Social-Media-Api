from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    RegisterView,
    PostListCreateView, PostDetailView,
    CommentListCreateView, CommentDetailView,
    LikeToggleView, FollowToggleView,
    FeedView
)

urlpatterns = [
    # Auth
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Posts
    path('posts/', PostListCreateView.as_view(), name='posts'),
    path('posts/<int:pk>/', PostDetailView.as_view(), name='post_detail'),

    # Comments
    path('comments/', CommentListCreateView.as_view(), name='comments'),
    path('comments/<int:pk>/', CommentDetailView.as_view(), name='comment_detail'),

    # Likes & Follows
    path('likes/', LikeToggleView.as_view(), name='like_toggle'),
    path('follow/', FollowToggleView.as_view(), name='follow_toggle'),

    # Feed
    path('feed/', FeedView.as_view(), name='feed'),
]
