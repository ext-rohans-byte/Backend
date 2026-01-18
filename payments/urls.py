from django.urls import path
from .views import PaymentCreateAPIView

urlpatterns = [
    path(
        "create/<int:order_id>/",
        PaymentCreateAPIView.as_view(),
        name="payment-create",
    ),
]
