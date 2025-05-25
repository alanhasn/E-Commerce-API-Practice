from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import generics
from django.db.models import Max
from .models import Product , Order , OrderItem
from .serializer import ProductSerializer , OrderSerializer , ProductInfoSerializer


class ProductListAPIView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ProductDetailAPIView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class OrderListAPIView(generics.ListAPIView):
    queryset = Order.objects.prefetch_related("items__product")
    serializer_class = OrderSerializer

class UserOrderListAPIView(generics.ListAPIView):
    queryset = Order.objects.prefetch_related("items__product") 
    serializer_class = OrderSerializer

    # for customize the data we get from database before send it to serializer
    def get_queryset(self):
        qs=super().get_queryset() # get the queryset data
        return qs.filter(user = self.request.user) # filter the data for Each user


@api_view(["GET"])
def product_info(request):
    products = Product.objects.all()
    serializer = ProductInfoSerializer({
        "products":products,
        "count":len(products),
        "max_price": products.aggregate(max_price=Max("price"))["max_price"]
    })
    return Response(serializer.data)

