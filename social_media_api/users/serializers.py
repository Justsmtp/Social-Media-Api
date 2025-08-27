# users/serializers.py
from rest_framework import serializers
from django.contrib.auth import get_user_model
from posts.models import Post

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, style={'input_type': 'password'}
    )

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'bio', 'profile_picture']
        read_only_fields = ['id']

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user


class MinimalPostSerializer(serializers.ModelSerializer):
    """Lightweight post serializer to avoid circular import"""
    class Meta:
        model = Post
        fields = ['id', 'title', 'created_at']


class UserSerializer(serializers.ModelSerializer):
    followers_count = serializers.IntegerField(source='followers.count', read_only=True)
    following_count = serializers.IntegerField(source='following.count', read_only=True)
    posts = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'bio', 'profile_picture',
            'followers_count', 'following_count', 'posts'
        ]

    def get_posts(self, obj):
        qs = Post.objects.filter(author=obj).order_by('-created_at')[:20]
        return MinimalPostSerializer(qs, many=True).data
