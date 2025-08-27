# notifications/serializers.py
from rest_framework import serializers
from .models import Notification
from django.contrib.auth import get_user_model
from posts.models import Post, Comment

User = get_user_model()


class SimpleUserSerializer(serializers.ModelSerializer):
    """Lightweight user serializer to avoid circular imports"""
    class Meta:
        model = User
        fields = ['id', 'username', 'profile_picture']


class MinimalPostSerializer(serializers.ModelSerializer):
    """Lightweight post serializer"""
    class Meta:
        model = Post
        fields = ['id', 'title', 'created_at']


class MinimalCommentSerializer(serializers.ModelSerializer):
    """Lightweight comment serializer"""
    class Meta:
        model = Comment
        fields = ['id', 'content', 'created_at']


class NotificationSerializer(serializers.ModelSerializer):
    actor = SimpleUserSerializer(read_only=True)
    post = MinimalPostSerializer(read_only=True)
    comment = MinimalCommentSerializer(read_only=True)

    class Meta:
        model = Notification
        fields = [
            'id',
            'recipient',
            'actor',
            'verb',
            'post',
            'comment',
            'timestamp',
            'is_read',
        ]
        read_only_fields = ['timestamp']
