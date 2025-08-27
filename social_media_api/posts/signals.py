# posts/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Like, Comment
from notifications.utils import create_notification

@receiver(post_save, sender=Like)
def like_created(sender, instance, created, **kwargs):
    if created and instance.post.author != instance.user:
        create_notification(
            recipient=instance.post.author,
            actor=instance.user,
            verb='liked your post',
            target=instance.post
        )

@receiver(post_save, sender=Comment)
def comment_created(sender, instance, created, **kwargs):
    if created and instance.post.author != instance.author:
        create_notification(
            recipient=instance.post.author,
            actor=instance.author,
            verb='commented on your post',
            target=instance.post
        )
