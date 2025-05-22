from django.urls import path
from .views import *


urlpatterns = [
    path("products/" , product_list),
    path('products/<int:pk>/', product_details),
    path("products/info/",product_info),
    path("orders/" , order_list),
]
