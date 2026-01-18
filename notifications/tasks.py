from celery import shared_task
from django.db import transaction,models
from django.db.utils import OperationalError

from .models import Notification
from .gateways.mock import MockNotificationGateway


@shared_task(bind=True, max_retries=3)
def send_notification_task(self, notification_id):
    try:
        # 🔒 Transaction REQUIRED for select_for_update
        with transaction.atomic():
            notification = (
                Notification.objects
                .select_for_update()
                .get(id=notification_id)
            )

            # Idempotency guard
            if notification.is_sent:
                return

            gateway = MockNotificationGateway()
            gateway.send(
                user=notification.user,
                message=notification.message,
            )

            notification.is_sent = True
            notification.save(update_fields=["is_sent"])

    except OperationalError as exc:
        # DB-level issues → retry
        raise self.retry(exc=exc, countdown=5)

    except Exception as exc:
        # External service failure → increment retry_count
        Notification.objects.filter(id=notification_id).update(
            retry_count=models.F("retry_count") + 1
        )
        raise self.retry(exc=exc, countdown=5)
