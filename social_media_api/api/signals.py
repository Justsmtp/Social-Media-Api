from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Like, Comment, Follow, Notification


@receiver(post_save, sender=Like)
def create_like_notification(sender, instance, created, **kwargs):
    if created and instance.post.user != instance.user:
        Notification.objects.create(
            sender=instance.user,
            receiver=instance.post.user,
            notification_type="like",
            post=instance.post,
        )


@receiver(post_save, sender=Comment)
def create_comment_notification(sender, instance, created, **kwargs):
    if created and instance.post.user != instance.user:
        Notification.objects.create(
            sender=instance.user,
            receiver=instance.post.user,
            notification_type="comment",
            post=instance.post,
            comment=instance,
        )


@receiver(post_save, sender=Follow)
def create_follow_notification(sender, instance, created, **kwargs):
    if created and instance.following != instance.follower:
        Notification.objects.create(
            sender=instance.follower,
            receiver=instance.following,
            notification_type="follow",
        )
