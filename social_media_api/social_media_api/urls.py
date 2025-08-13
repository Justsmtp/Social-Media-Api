"""
URL configuration for social_media_api project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from api.views import (
    RegisterView, PostListCreateView, PostDetailView,
    CommentListCreateView, CommentDetailView,
    LikeToggleView, FollowToggleView, FeedView
)

urlpatterns = [
    path('admin/', admin.site.urls),

    # Auth
    path('api/register/', RegisterView.as_view(), name='register'),
    path('api/login/', TokenObtainPairView.as_view(), name='login'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Posts
    path('api/posts/', PostListCreateView.as_view(), name='posts'),
    path('api/posts/<int:pk>/', PostDetailView.as_view(), name='post_detail'),

    # Comments
    path('api/comments/', CommentListCreateView.as_view(), name='comments'),
    path('api/comments/<int:pk>/', CommentDetailView.as_view(), name='comment_detail'),

    # Likes & Follows
    path('api/likes/', LikeToggleView.as_view(), name='like_toggle'),
    path('api/follow/', FollowToggleView.as_view(), name='follow_toggle'),

    # Feed
    path('api/feed/', FeedView.as_view(), name='feed'),
]
