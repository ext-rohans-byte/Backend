from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from django.core.exceptions import ValidationError

from .models import Order
from .serializers import OrderReadSerializer
from .dto import CreateOrderData, OrderItemData
from .services import create_order


class OrderCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            items_data = request.data.get("items",[])
            address = request.data.get("address")
            pincode = request.data.get("pincode")


            if not items_data:
                return Response(
                    {"error":"Order must contain at least one item."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            
            if not address or not pincode:
                return Response(
                    {"error":"Address and pincode are required"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            items = [
                OrderItemData(
                    product_id = item["product_id"],
                    quantity=item["quantity"],
                )
                for item in items_data
            ]

            order_data = CreateOrderData(
                items=items,
                address=address,
                pincode=pincode
                )

            order = create_order(
                user=request.user,
                order_data=order_data
            )
            
            return Response(
                {"order_id":order.id},
                status=status.HTTP_201_CREATED,
            )
        
        except KeyError:
            return Response(
                {"error":"Invalid request format."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except ValidationError as e:
            return Response(
                {"error":e.message},
                status=status.HTTP_400_BAD_REQUEST,
            )

class OrderListAPIView(ListAPIView):
    serializer_class = OrderReadSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)
