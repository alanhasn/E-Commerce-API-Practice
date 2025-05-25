from django.urls import path
from .views import (
    ProductInfoAPIView , 
    ProductDetailAPIView ,
    ProductListAPIView ,
    OrderListAPIView , 
    UserOrderListAPIView,
)


urlpatterns = [
    path("products/" , ProductListAPIView.as_view()),
    path('products/<int:pk>/', ProductDetailAPIView.as_view()),
    path("products/info/",ProductInfoAPIView.as_view()),
    path("orders/" , OrderListAPIView.as_view()),
    path('user-orders/', UserOrderListAPIView.as_view(), name="user-orders"),
]
