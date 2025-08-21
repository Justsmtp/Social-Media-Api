"""
This module defines all API endpoints and routes them to appropriate views.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    RegisterView,
    PostViewSet, CommentViewSet,
    LikeViewSet, FollowViewSet,
    FeedView, NotificationViewSet
)

# Create router and register viewsets
router = DefaultRouter()

# Register all viewsets with the router
router.register("posts", PostViewSet, basename="posts")
router.register("comments", CommentViewSet, basename="comments")
router.register("likes", LikeViewSet, basename="likes")
router.register("follows", FollowViewSet, basename="follows")
router.register("notifications", NotificationViewSet, basename="notifications")

# Define URL patterns
urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("", include(router.urls)),
    path("feed/", FeedView.as_view(), name="feed"),
]
