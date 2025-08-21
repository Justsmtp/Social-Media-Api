from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from .models import Post, Comment, Like, Follow, Notification

User = get_user_model()


class SocialMediaApiTests(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username="alice", password="password123")
        self.user2 = User.objects.create_user(username="bob", password="password123")
        self.client.login(username="alice", password="password123")

    def test_register(self):
        url = reverse("register")
        resp = self.client.post(url, {"username": "charlie", "password": "Newuserpass123!"})
        self.assertIn(resp.status_code, (status.HTTP_201_CREATED, status.HTTP_400_BAD_REQUEST))

    def test_create_post(self):
        url = reverse("posts-list")
        resp = self.client.post(url, {"content": "Hello World!"})
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 1)

    def test_comment_creates_notification(self):
        post = Post.objects.create(user=self.user2, content="Post content")
        url = reverse("comments-list")
        resp = self.client.post(url, {"post": post.id, "text": "Nice post!"})
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Comment.objects.count(), 1)
        self.assertEqual(Notification.objects.filter(receiver=self.user2, notification_type="comment").count(), 1)

    def test_like_toggle_and_notification(self):
        post = Post.objects.create(user=self.user2, content="Post content")
        url = reverse("likes-list")
        resp = self.client.post(url, {"post": post.id})
        self.assertIn(resp.status_code, (status.HTTP_201_CREATED, status.HTTP_200_OK))
        self.assertEqual(Like.objects.count(), 1)
        self.assertEqual(Notification.objects.filter(receiver=self.user2, notification_type="like").count(), 1)

        resp2 = self.client.post(url, {"post": post.id})  # unlike
        self.assertEqual(Like.objects.count(), 0)

    def test_follow_toggle_and_notification(self):
        url = reverse("follows-list")
        resp = self.client.post(url, {"following": self.user2.id})
        self.assertIn(resp.status_code, (status.HTTP_201_CREATED, status.HTTP_200_OK))
        self.assertEqual(Follow.objects.count(), 1)
        self.assertEqual(Notification.objects.filter(receiver=self.user2, notification_type="follow").count(), 1)

        resp2 = self.client.post(url, {"following": self.user2.id})  # unfollow
        self.assertEqual(Follow.objects.count(), 0)

    def test_feed_requires_auth(self):
        self.client.logout()
        url = reverse("feed")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)
