from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from django.db.models import Max
from api.models import Product , Order
from api.serializer import ProductSerializer , OrderSerializer , ProductInfoSerializer
from api.filters import ProductFilter , IsOnStuckFilterBackend
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import(
    IsAuthenticated ,
    IsAdminUser,
    AllowAny
) 
from rest_framework.pagination import LimitOffsetPagination
from api.pagination import CustomPageNumberPagination , CustomLimitOffsetPagination , CustomCursorPagination

class ProductListCreateAPIView(generics.ListCreateAPIView):
    queryset = Product.objects.order_by("pk") # order by primary key
    serializer_class = ProductSerializer
    filterset_class = ProductFilter
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
        IsOnStuckFilterBackend,
    ]
    search_fields = ['name',"description"]
    ordering_fields = ['name','price' , "stock"]
    pagination_class = CustomPageNumberPagination # set the Custom pagination class
    
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
    pagination_class = CustomLimitOffsetPagination# set the Custom limit pagination class

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

