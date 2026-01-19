from django.urls import path
from .views import (
    ProductListAPIView,
    ProductDetailAPIView,
    ProductCreateAPIView,
)

urlpatterns = [
    path("", ProductListAPIView.as_view()),
    path("<int:pk>/", ProductDetailAPIView.as_view()),
    path("create/", ProductCreateAPIView.as_view()),
]
