from django.contrib import admin
from .models import Product
# Register your models here.

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display=(
        "id",
        "name",
        "sku",
        "price",
        "stock_quantity",
        "is_active",
    )
    search_fields = ("name","sku")
    list_filter = ("is_active",)