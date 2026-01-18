from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from orders.models import Order
from .services import create_payment

from django.shortcuts import get_object_or_404

class PaymentCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, order_id):
        order = get_object_or_404(
            Order,
            id=order_id,
            user=request.user
        )
        if hasattr(order, "payment"):
            return Response(
                {"detail": "Payment already completed for this order"},
                status=status.HTTP_409_CONFLICT,
            )

        payment = create_payment(order=order)

        return Response(
            {
                "payment_id": payment.id,
                "status": payment.status,
                "order_status": order.status,
            },
            status=status.HTTP_201_CREATED,
        )