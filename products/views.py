from rest_framework import generics, permissions
from django.core.cache import cache
from .models import Product
from .serializers import ProductSerializer
from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver


class ProductListAPIView(generics.ListAPIView):
    serializer_class = ProductSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        user = self.request.user
        cache_key = "products:list"

        # Check if cached data exists
        products = cache.get(cache_key)
        if products:
            return products

        # Admin / Staff → all products
        if user.is_authenticated and user.is_staff:
            products = Product.objects.all().order_by("id")
        else:
            # User / Anonymous → only active products
            products = Product.objects.filter(is_active=True).order_by("id")

        # Cache the result for 5 minutes (300 seconds)
        cache.set(cache_key, products, timeout=300)

        return products


class ProductDetailAPIView(generics.RetrieveAPIView):
    serializer_class = ProductSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        user = self.request.user
        pk = self.kwargs["pk"]
        cache_key = f"products:{pk}"

        # Try to get the cached product data
        product = cache.get(cache_key)
        if product:
            return [product]  # return as a list to satisfy queryset

        if user.is_authenticated and user.is_staff:
            product = Product.objects.filter(id=pk).first()
        else:
            product = Product.objects.filter(is_active=True, id=pk).first()

        # Cache the product detail for 5 minutes
        if product:
            cache.set(cache_key, product, timeout=300)

        return [product] if product else Product.objects.none()


class ProductCreateAPIView(generics.CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAdminUser]

    def perform_create(self, serializer):
        # Create the product and then invalidate cache
        product = serializer.save()

        # Invalidate list and detail cache when a product is created
        cache.delete("products:list")
        cache.delete(f"products:{product.id}")


# Signal to invalidate cache during product updates
@receiver(pre_save, sender=Product)
def invalidate_product_cache(sender, instance, **kwargs):
    if instance.id:
        cache.delete(f"products:{instance.id}")  # Invalidate cache before saving
    cache.delete("products:list")  # Clear the list cache to fetch the updated data


# Signal to invalidate cache on product deletion
@receiver(post_delete, sender=Product)
def invalidate_product_cache_on_delete(sender, instance, **kwargs):
    cache.delete(f"products:{instance.id}")  # Invalidate product cache
    cache.delete("products:list")  # Clear the product list cache


