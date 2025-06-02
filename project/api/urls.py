from django.urls import path
from .views import (
    ProductInfoAPIView , 
    ProductDetailAPIView ,
    ProductListCreateAPIView ,
    OrderListAPIView , 
    UserOrderListAPIView,
)


urlpatterns = [
    path("products/" , ProductListCreateAPIView.as_view()),
    path('products/<int:pk>/', ProductDetailAPIView.as_view()),
    path("products/info/",ProductInfoAPIView.as_view()),
    path("orders/" , OrderListAPIView.as_view()),
    path('user-orders/', UserOrderListAPIView.as_view(), name="user-orders"),
]
