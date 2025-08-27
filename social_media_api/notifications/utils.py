# notifications/utils.py
from .models import Notification
from django.contrib.contenttypes.models import ContentType

def create_notification(recipient, actor, verb, target=None):
    """
    Creates a Notification record. Accepts a model instance target or None.
    """
    nc = None
    if target is not None:
        content_type = ContentType.objects.get_for_model(target.__class__)
        nc = Notification.objects.create(
            recipient=recipient,
            actor=actor,
            verb=verb,
            target_content_type=content_type,
            target_object_id=target.pk
        )
    else:
        nc = Notification.objects.create(recipient=recipient, actor=actor, verb=verb)
    return nc
