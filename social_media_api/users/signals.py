from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.conf import settings
from notifications.utils import create_notification

User = settings.AUTH_USER_MODEL

# Because CustomUser.following is a M2M to self, listen for m2m_changed
from django.apps import apps
CustomUser = apps.get_model('users', 'CustomUser')

@receiver(m2m_changed, sender=CustomUser.following.through)
def following_changed(sender, instance, action, reverse, model, pk_set, **kwargs):
    # action can be 'post_add' when following occurs
    if action == 'post_add' and pk_set:
        for pk in pk_set:
            followed_user = CustomUser.objects.get(pk=pk)
            # create a follow notification
            create_notification(
                recipient=followed_user,
                actor=instance,
                verb='followed you',
                target=None
            )
