from celery import shared_task
from django.core.exceptions import ObjectDoesNotExist

from .models import Notification
from .email_templates import build_email
from .gateways import EmailNotificationGateway


@shared_task(bind=True, max_retries=3)
def send_notification_task(self, notification_id):
    try:
        notification = Notification.objects.get(id=notification_id)

        if notification.is_sent:
            return  # idempotent

        email_data = build_email(
            event=notification.event,
            payload=notification.payload,
        )

        gateway = EmailNotificationGateway()
        gateway.send(
            user=notification.user,
            subject=email_data["subject"],
            message=email_data["body"],
        )

        notification.is_sent = True
        notification.save(update_fields=["is_sent"])

    except ObjectDoesNotExist:
        # Notification deleted → don't retry
        return

    except Exception as exc:
        notification.retry_count += 1
        notification.save(update_fields=["retry_count"])
        raise self.retry(exc=exc, countdown=5)
