from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import (OrderViewSet, ProductDetailAPIView, ProductInfoAPIView,
                    ProductListCreateAPIView)

urlpatterns = [
    # Define the URL patterns for the API endpoints
    path("products/" , ProductListCreateAPIView.as_view()),
    path('products/<int:pk>/', ProductDetailAPIView.as_view()),
    path("products/info/",ProductInfoAPIView.as_view()),
]

router = DefaultRouter()
router.register("orders" , OrderViewSet)
urlpatterns += router.urls
