from rest_framework import serializers

from .models import Order, OrderItem, Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            "name",
            "description",
            "price",
            "stock",
            "image"
        ]
    
    # Validate that the price is greater than 0
    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                "Price must be greater than 0."
            )
        return value

    # Validate that the stock is greater than 0
    def validate_stock(self , value):
        if value <= 0:
            raise serializers.ValidationError(
                "Stock must be greater than 0."
            )
        return value


class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source = "product.name")
    product_price = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        source = "product.price")
    class Meta:
        model = OrderItem
        fields = [
            "product_name" ,
            "product_price",
            "quantity",
            "item_subtotal"
            ]

# This serializer is used to create an order with multiple items
class OrderCreateSerializer(serializers.ModelSerializer): 
    # Nested serializer for order items
    class OrderItemCreateSerializer(serializers.ModelSerializer):

        # Validate that the quantity is less than or equal to the product stock
        def validate(self, data):
            product = data['product']
            quantity = data['quantity']
            if quantity > product.stock:
                raise serializers.ValidationError(
                    f"Not enough stock. Available: {product.stock}, Requested: {quantity}"
                )
            return data

        class Meta:
            model = OrderItem
            fields = ('product', 'quantity')

    order_id = serializers.UUIDField(read_only=True)
    items = OrderItemCreateSerializer(many=True)

    class Meta:
        model = Order
        fields = [
            "order_id",
            "user",
            "status",
            "items"
        ]
        extra_kwargs = {
            'user': {'read_only': True},
        }

    def create(self, validated_data):
        order_items_data = validated_data.pop('items')
        order = Order.objects.create(**validated_data)

        for item_data in order_items_data:
            OrderItem.objects.create(order=order, **item_data)
        return order
    
class OrderSerializer(serializers.ModelSerializer):
    order_id = serializers.UUIDField(read_only=True)
    items = OrderItemSerializer(many = True , read_only=True)
    total_price = serializers.SerializerMethodField(method_name="total")

    def total(self, obj):
        items = obj.items.all()
        return sum(item.item_subtotal for item in items)
    
    class Meta:
        model = Order
        fields = [
            "order_id",
            "user",
            "created_at",
            "status",
            "items",
            "total_price"
        ]

class ProductInfoSerializer(serializers.Serializer):
    products = ProductSerializer(many=True)
    count = serializers.IntegerField()
    max_price = serializers.FloatField()

