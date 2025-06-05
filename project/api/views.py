from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.permissions import(
    IsAuthenticated ,
    IsAdminUser,
    AllowAny
) 
from django.db.models import Max
from .models import Product , Order
from .serializer import ProductSerializer , OrderSerializer , ProductInfoSerializer


class ProductListCreateAPIView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    # customize the permissions for this view(just admin can create new products)
    # but all users can see the products
    def get_permissions(self):
        self.permission_classes = [AllowAny]
        if self.request.method == "POST":
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()

class ProductDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_permissions(self):
        self.permission_classes = [AllowAny]
        if self.request.method in ["PUT", "PATCH", "DELETE"]:
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()

class OrderListAPIView(generics.ListAPIView):
    queryset = Order.objects.prefetch_related("items__product")
    serializer_class = OrderSerializer

class UserOrderListAPIView(generics.ListAPIView):
    queryset = Order.objects.prefetch_related("items__product") 
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated] # the user should be authenticated to access this view

    # for customize the data we get from database before send it to serializer
    def get_queryset(self):
        qs=super().get_queryset() # get the queryset data
        return qs.filter(user = self.request.user) # filter the data for Each user

class ProductInfoAPIView(APIView):
    def get(self , request):
        products = Product.objects.all()
        serializer = ProductInfoSerializer({
            "products":products,
            "count":len(products),
            "max_price": products.aggregate(max_price=Max("price"))["max_price"]
        })
        return Response(serializer.data)

