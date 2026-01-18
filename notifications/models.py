from django.db import models
from django.conf import settings


class Notification(models.Model):
    EVENT_CHOICES = (
        ("order_created", "Order Created"),
        ("payment_success", "Payment Success"),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="notifications",
    )

    event = models.CharField(
        max_length=50,
        choices=EVENT_CHOICES,
    )

    message = models.TextField()

    is_sent = models.BooleanField(default=False)
    retry_count = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.event}"
