from django.urls import path
from .views import OrderCreateAPIView,OrderListAPIView

urlpatterns = [
    path("create/", OrderCreateAPIView.as_view()),
    path("", OrderListAPIView.as_view())
]