from .models import Notification
from .tasks import send_notification_task

def create_notification(*, user, event, message):
    notification = Notification.objects.create(
        user=user,
        event=event,
        message=message,
    )

    send_notification_task.delay(notification.id)

    return notification
