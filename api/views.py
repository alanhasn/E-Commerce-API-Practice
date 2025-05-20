from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Product , Order , OrderItem
from .serializer import ProductSerializer

@api_view(["GET"])
def product_list(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products , many = True)
    return Response(serializer.data)

@api_view(["GET"])
def product_details(request,pk):
    product = get_object_or_404(Product , pk=pk)
    serializer = ProductSerializer(product)
    return Response(serializer.data)


# def order_list(request):
#     order = Order.objects.all()
#     serializer = OrderSerializer(order , many=True)
#     return JsonResponse({
#         "data" : serializer.data
#     })