from django.urls import path
from .views import *


urlpatterns = [
    path("products/" , product_list),
    path('products/<int:pk>/', product_details),
    # path('orders/', order_list),
]