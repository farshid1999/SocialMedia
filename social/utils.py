from .models import Notification
from django.contrib.contenttypes.models import ContentType

def create_notification(recipient, actor, verb, target=None):
    notification = Notification(
        recipient=recipient,
        actor=actor,
        verb=verb,
    )
    if target:
        notification.content_type = ContentType.objects.get_for_model(target)
        notification.object_id = target.pk
    notification.save()

