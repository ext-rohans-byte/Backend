from django.db import transaction
from django.core.exceptions import ValidationError
from orders.models import Order
from .models import Payment
from .gateways.mock import MockPaymentGateway
from notifications.services import create_notification



def create_payment(*, order):
    if Payment.objects.filter(order=order).exists():
        raise ValidationError("Payment already exists for this order.")

    if order.status == "paid":
        raise ValidationError("Order already paid.")

    gateway = MockPaymentGateway()

    with transaction.atomic():
        payment = Payment.objects.create(
            order=order,
            amount=order.total_amount,
            status="initiated",
        )

        result = gateway.charge(float(order.total_amount))

        if result["status"] == "success":
            payment.status = "success"
            payment.provider_reference = result["reference"]
            order.status = Order.STATUS_PAID

            create_notification(
                user=order.user,
                event="payment_success",
                message=f"Payment successful for Order #{order.id}"
            )

        else:
            payment.status = "failed"
            order.status = "created"

        payment.save()
        order.save()

    return payment
