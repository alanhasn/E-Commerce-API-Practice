from django.urls import path
from .views import (
    product_info , 
    ProductDetailAPIView ,
    ProductListAPIView ,
    OrderListAPIView , 
    UserOrderListAPIView,
)


urlpatterns = [
    path("products/" , ProductListAPIView.as_view()),
    path('products/<int:pk>/', ProductDetailAPIView.as_view()),
    path("products/info/",product_info),
    path("orders/" , OrderListAPIView.as_view()),
    path('user-orders/', UserOrderListAPIView.as_view(), name="user-orders"),
]
