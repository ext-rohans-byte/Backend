from django.db import transaction
from django.core.exceptions import ValidationError
from notifications.services import create_notification
from products.models import Product
from .models import Order, OrderItem
from .dto import CreateOrderData


def create_order(*, user, order_data: CreateOrderData) -> Order:
    with transaction.atomic():
        total_amount = 0

        order = Order.objects.create(
            user=user,
            address=order_data.address,
            pincode=order_data.pincode,
            total_amount=0,
        )

        for item in order_data.items:
            try:
                product = Product.objects.select_for_update().get(
                    id=item.product_id,
                    is_active=True
                )
            except Product.DoesNotExist:
                raise ValidationError("Invalid or inactive product.")

            if item.quantity <= 0:
                raise ValidationError("Quantity must be greater than zero.")

            if product.stock_quantity < item.quantity:
                raise ValidationError(
                    f"Insufficient stock for {product.name}."
                )

            product.stock_quantity -= item.quantity
            product.save()

            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=item.quantity,
                price_at_purchase=product.price,
            )

            total_amount += product.price * item.quantity

        order.total_amount = total_amount
        order.save()

        create_notification(
            user=order.user,
            event="order_created",
            message="Order created successfully",
            payload={
                "order_id": order.id,
                "total_amount": str(order.total_amount),
                "address": order.address,
                "items": [
                    {
                        "name": item.product.name,
                        "qty": item.quantity,
                        "price": str(item.price_at_purchase),
                    }
                    for item in order.items.all()
                ],
            },
        )

        return order
