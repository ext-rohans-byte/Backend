from .models import Notification
from .tasks import send_notification_task


def create_notification(*, user, event, message, payload=None):
    notification = Notification.objects.create(
        user=user,
        event=event,
        message=message,
        payload=payload or {},
    )

    send_notification_task.delay(notification.id)
    return notification
