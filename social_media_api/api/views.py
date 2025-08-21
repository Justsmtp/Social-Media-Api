from django.contrib.auth import get_user_model
from django.db.models import Count, F
from django.shortcuts import get_object_or_404

from rest_framework import generics, permissions, status, filters, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action

from .models import Post, Comment, Like, Follow, Notification
from .serializers import (
    RegisterSerializer, PostSerializer, CommentSerializer,
    LikeSerializer, FollowSerializer, FollowWriteSerializer,
    NotificationSerializer
)
from .permissions import IsOwnerOrReadOnly

User = get_user_model()


# USER REGISTRATION
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]


# POSTS
class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['content']
    ordering_fields = ['created_at', 'likes_count', 'comments_count', 'popularity']
    ordering = ['-created_at']

    def get_queryset(self):
        qs = Post.objects.all().select_related('user').annotate(
            likes_count=Count('likes', distinct=True),
            comments_count=Count('comments', distinct=True)
        )
        user_id = self.request.query_params.get('user')
        if user_id:
            qs = qs.filter(user_id=user_id)
        return qs.annotate(popularity=F('likes_count') + F('comments_count'))

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# COMMENTS
class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['created_at']
    ordering = ['created_at']

    def get_queryset(self):
        qs = Comment.objects.select_related('user', 'post')
        post_id = self.request.query_params.get('post')
        if post_id:
            qs = qs.filter(post_id=post_id)
        return qs

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# LIKES (toggle)
class LikeViewSet(viewsets.GenericViewSet, generics.CreateAPIView, generics.DestroyAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        post = get_object_or_404(Post, id=self.request.data.get('post'))
        like, created = Like.objects.get_or_create(user=self.request.user, post=post)
        if not created:
            like.delete()
            self._was_unliked = True
        else:
            self._was_unliked = False

    def create(self, request, *args, **kwargs):
        self._was_unliked = False
        super().create(request, *args, **kwargs)
        return Response(
            {"message": "Unliked" if self._was_unliked else "Liked"},
            status=status.HTTP_200_OK if self._was_unliked else status.HTTP_201_CREATED
        )


# FOLLOWS (toggle)
class FollowViewSet(viewsets.GenericViewSet, generics.CreateAPIView, generics.DestroyAPIView):
    queryset = Follow.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action == "create":
            return FollowWriteSerializer
        return FollowSerializer

    def perform_create(self, serializer):
        following_id = self.request.data.get('following')
        to_follow = get_object_or_404(User, id=following_id)
        if to_follow == self.request.user:
            raise PermissionError("You cannot follow yourself.")

        follow, created = Follow.objects.get_or_create(
            follower=self.request.user,
            following=to_follow
        )
        if not created:
            follow.delete()
            self._was_unfollowed = True
        else:
            self._was_unfollowed = False

    def create(self, request, *args, **kwargs):
        self._was_unfollowed = False
        super().create(request, *args, **kwargs)
        return Response(
            {"message": "Unfollowed" if self._was_unfollowed else "Followed"},
            status=status.HTTP_200_OK if self._was_unfollowed else status.HTTP_201_CREATED
        )


# FEED
class FeedView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['created_at', 'likes_count', 'comments_count', 'popularity']
    ordering = ['-created_at']

    def get_queryset(self):
        followed_ids = self.request.user.following.values_list('following_id', flat=True)
        base = Post.objects.filter(user_id__in=followed_ids).select_related('user').annotate(
            likes_count=Count('likes', distinct=True),
            comments_count=Count('comments', distinct=True)
        )
        return base.annotate(popularity=F('likes_count') + F('comments_count'))


# NOTIFICATIONS
class NotificationViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(receiver=self.request.user).order_by("-created_at")

    @action(detail=False, methods=["post"])
    def mark_as_read(self, request):
        Notification.objects.filter(receiver=request.user, is_read=False).update(is_read=True)
        return Response({"status": "notifications marked as read"})
