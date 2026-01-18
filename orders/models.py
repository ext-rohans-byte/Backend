from django.db import models
from products.models import Product
from django.contrib.auth import get_user_model
from django.conf import settings


User = get_user_model()

class Order(models.Model):
    STATUS_PENDING = "PENDING"
    STATUS_PAID = "PAID"
    STATUS_CANCELLED = "CANCELLED"

    STATUS_CHOICES = [
        (STATUS_PENDING,"Pending"),
        (STATUS_PAID,"Paid"),
        (STATUS_CANCELLED,"Cancelled")
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    status = models.CharField(max_length = 20,choices=STATUS_CHOICES,default = "PENDING")
    total_amount = models.DecimalField(max_digits=10,decimal_places=2)
    address = models.TextField(null=True, blank=True)
    pincode = models.CharField(max_length=10, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"Order {self.id}"
    

class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        related_name="items",
        on_delete=models.CASCADE
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT
    )
    quantity = models.PositiveIntegerField()
    price_at_purchase = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )