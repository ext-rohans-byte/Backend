from rest_framework import generics, permissions
from .models import Product
from .serializers import ProductSerializer


class ProductListAPIView(generics.ListAPIView):
    serializer_class = ProductSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        user = self.request.user

        # Admin / Staff → all products
        if user.is_authenticated and user.is_staff:
            return Product.objects.all().order_by("id")

        # User / Anonymous → only active products
        return Product.objects.filter(is_active=True).order_by("id")

class ProductDetailAPIView(generics.RetrieveAPIView):
    serializer_class = ProductSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        user = self.request.user

        if user.is_authenticated and user.is_staff:
            return Product.objects.all()

        return Product.objects.filter(is_active=True)

class ProductCreateAPIView(generics.CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAdminUser]
