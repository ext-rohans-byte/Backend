from rest_framework import serializers
from .models import Payment

class PaymentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ("order",)
    
    def validate_order(self, order):
        if hasattr(order,"payment"):
            raise serializers.ValidationError(
                "Payment already exists for this order."
            )
        return order