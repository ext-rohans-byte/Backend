from rest_framework import serializers
from products.models import Product
from .models import Order,OrderItem

class OrderItemInputSerializer(serializers.Serializer):
    product_id = serializers.PrimaryKeyRelatedField(
        queryset = Product.objects.filter(is_active=True)
    )
    quantity = serializers.IntegerField(min_value=1)

class OrderCreateSerializer(serializers.Serializer):
    address = serializers.CharField(max_length=500)
    pincode = serializers.CharField(max_length=10)
    items = OrderItemInputSerializer(many=True)

    def validate_items(self,items):
        if not items:
            raise serializers.ValidationError("" \
            "Order must contain at least one item"
            )
        
        product_ids = [item["product_id"].id for item in items]
        if len(product_ids) != len(set(product_ids)):
            raise serializers.ValidationError(
                "Duplicate products are not allowed."
            )
        
        return items

class OrderItemReadSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(
        source="product.name",
        read_only=True
    )

    class Meta:
        model = OrderItem
        fields = (
            "id",
            "product_name",
            "quantity",
            "price_at_purchase",
        )

class OrderReadSerializer(serializers.ModelSerializer):
    items = OrderItemReadSerializer(many=True, read_only = True)

    class Meta:
        model = Order
        fields = (
            "id",
            "status",
            "total_amount",
            "created_at",
            "items",
        )