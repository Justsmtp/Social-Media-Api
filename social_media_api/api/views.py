from django.contrib.auth import get_user_model
from django.db.models import Count, F
from django.shortcuts import get_object_or_404

from rest_framework import generics, permissions, status, filters
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Post, Comment, Like, Follow
from .serializers import (
    RegisterSerializer, PostSerializer, CommentSerializer,
    LikeSerializer, FollowSerializer
)
from .permissions import IsOwnerOrReadOnly

User = get_user_model()

# --- USER REGISTRATION ---
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]


# --- POST CRUD ---
class PostListCreateView(generics.ListCreateAPIView):
    """
    GET: List posts with optional ?search=, ?ordering=, ?user=<id>
    POST: Create a post (auth required)
    """
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['content']
    ordering_fields = ['created_at', 'likes_count', 'comments_count']
    ordering = ['-created_at']

    def get_queryset(self):
        qs = Post.objects.all().select_related('user').annotate(
            likes_count=Count('likes', distinct=True),
            comments_count=Count('comments', distinct=True)
        )
        user_id = self.request.query_params.get('user')
        if user_id:
            qs = qs.filter(user_id=user_id)
        return qs

    def perform_create(self, serializer):
        if not self.request.user.is_authenticated:
            raise PermissionError("Authentication required.")
        serializer.save(user=self.request.user)


class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def get_queryset(self):
        return Post.objects.select_related('user').annotate(
            likes_count=Count('likes', distinct=True),
            comments_count=Count('comments', distinct=True)
        )


# --- COMMENT CRUD ---
class CommentListCreateView(generics.ListCreateAPIView):
    """
    GET: List comments (optionally filter by ?post=<id>)
    POST: Create comment (auth)
    """
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
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
        if not self.request.user.is_authenticated:
            raise PermissionError("Authentication required.")
        serializer.save(user=self.request.user)


class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all().select_related('user', 'post')
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]


# --- LIKE / UNLIKE ---
class LikeToggleView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        post_id = request.data.get('post_id')
        if not post_id:
            return Response({'detail': 'post_id is required.'}, status=400)
        post = get_object_or_404(Post, id=post_id)
        like, created = Like.objects.get_or_create(user=request.user, post=post)
        if not created:
            like.delete()
            return Response({"message": "Unliked"}, status=status.HTTP_200_OK)
        return Response({"message": "Liked"}, status=status.HTTP_201_CREATED)


# --- FOLLOW / UNFOLLOW ---
class FollowToggleView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user_id = request.data.get('user_id')
        if not user_id:
            return Response({'detail': 'user_id is required.'}, status=400)
        to_follow = get_object_or_404(User, id=user_id)
        if to_follow == request.user:
            return Response({"detail": "You cannot follow yourself."}, status=400)

        follow, created = Follow.objects.get_or_create(
            follower=request.user, following=to_follow
        )
        if not created:
            follow.delete()
            return Response({"message": "Unfollowed"}, status=200)
        return Response({"message": "Followed"}, status=201)


# --- FEED with Pagination + Sorting by Date/Popularity ---
class FeedView(generics.ListAPIView):
    """
    GET: Posts from followed users.
    Sorting:
      ?ordering=-created_at  (default)
      ?ordering=-popularity  (likes + comments)
    """
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['created_at', 'likes_count', 'comments_count', 'popularity']
    ordering = ['-created_at']

    def get_queryset(self):
        # IDs of users the current user follows
        followed_ids = self.request.user.following.values_list('following_id', flat=True)
        base = Post.objects.filter(user_id__in=followed_ids).select_related('user').annotate(
            likes_count=Count('likes', distinct=True),
            comments_count=Count('comments', distinct=True)
        )

        # Popularity metric: likes + comments (annotate as 'popularity')
        base = base.annotate(popularity=F('likes_count') + F('comments_count'))
        return base
