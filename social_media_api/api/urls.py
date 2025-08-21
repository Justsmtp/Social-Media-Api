from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    RegisterView,
    PostViewSet, CommentViewSet,
    LikeViewSet, FollowViewSet,
    FeedView, NotificationViewSet
)

router = DefaultRouter()
router.register("posts", PostViewSet, basename="posts")
router.register("comments", CommentViewSet, basename="comments")
router.register("likes", LikeViewSet, basename="likes")
router.register("follows", FollowViewSet, basename="follows")
router.register("notifications", NotificationViewSet, basename="notifications")

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("", include(router.urls)),
    path("feed/", FeedView.as_view(), name="feed"),
]
