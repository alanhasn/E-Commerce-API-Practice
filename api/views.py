from django.db.models import Max
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from api.filters import IsOnStuckFilterBackend, OrderFilter, ProductFilter
from api.models import Order, Product
from api.pagination import (CustomCursorPagination,
                            CustomLimitOffsetPagination,
                            CustomPageNumberPagination)
from api.serializer import (OrderSerializer, ProductInfoSerializer,
                            ProductSerializer , OrderCreateSerializer)


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
    
class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.prefetch_related("items__product")
    serializer_class = OrderSerializer
    pagination_class = CustomLimitOffsetPagination # set the Custom limit pagination class
    permission_classes = [IsAuthenticated]
    filterset_class = OrderFilter
    filter_backends = [DjangoFilterBackend]

    def get_serializer_class(self):
        # If the action is "create", use OrderItemSerializer
        # Otherwise, use the default OrderSerializer
        if self.request.method == "POST" and self.action == "create":
            return OrderCreateSerializer
        return super().get_serializer_class()

    # This method is used to filter the queryset based on the user
    # If the user is not staff, it will return only the orders related to that user
    def get_queryset(self):
        qs = super().get_queryset()
        if not self.request.user.is_staff:
            return qs.filter(user=self.request.user)
        return qs
    
    # This method is used to customize the response of the create action
    def perform_create(self, serializer):
        order = serializer.save(user=self.request.user)
        # Update product stock
        for item in order.items.all():
            product = item.product
            product.stock -= item.quantity
            product.save()
        return order

class ProductInfoAPIView(APIView):
    def get(self, request):
        try:
            products = Product.objects.all()
            if not products.exists():
                return Response({"message": "No products found"}, status=404)
                
            serializer = ProductInfoSerializer({
                "products": products,
                "count": products.count(),
                # Get the maximum price of the products
                "max_price": products.aggregate(max_price=Max("price"))["max_price"] or 0
            })
            return Response(serializer.data)
        except Exception as e:
            return Response({"error": str(e)}, status=500)

