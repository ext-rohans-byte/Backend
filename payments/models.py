from django.db import models
from orders.models import Order

class Payment(models.Model):
    STATUS_CHOICES = (
        ("initiated", "Initiated"),
        ("success", "Success"),
        ("failed", "Failed"),
    )

    order = models.OneToOneField(
        Order,
        on_delete=models.CASCADE,
        related_name="payment",
    )

    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="initiated",
    )

    provider_reference = models.CharField(
        max_length=255,
        blank=True,
        null=True,
    )

    created_at = models.DateTimeField(auto_now_add=True)
