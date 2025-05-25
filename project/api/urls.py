from django.urls import path
from .views import *


urlpatterns = [
    path("products/" , ProductListAPIView.as_view()),
    path('products/<int:pk>/', ProductDetailAPIView.as_view()),
    path("products/info/",product_info),
    path("orders/" , OrderListAPIView.as_view()),
]
