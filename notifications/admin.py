from django.contrib import admin
from .models import Notification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "event",
        "is_sent",
        "retry_count",
        "created_at",
    )
    list_filter = ("event", "is_sent")
    search_fields = ("user__username", "message")
