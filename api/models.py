from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

class User(AbstractUser):
    pass

class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=8 , decimal_places=2)
    stock = models.PositiveIntegerField()
    image = models.ImageField(upload_to="Products/" , null=True , blank=True)

    # This property checks if the product is in stock
    @property
    def in_stock(self) -> bool:
        return self.stock > 0
    
    def __str__(self):
        return self.name

class Order(models.Model):
    class OrdedrStatus(models.TextChoices):
        PENDING = "Pending"
        CONFIRMED = "Confirmed"
        CANCELLED = "Cancelled"

    order_id = models.UUIDField(primary_key=True ,default=uuid.uuid4) # Unique identifier for the order
    user = models.ForeignKey(User , on_delete=models.CASCADE , related_name="user") # related to the user who placed the order
    created_at = models.DateTimeField(auto_now_add=True , null=True , blank=True)
    status = models.CharField(
        choices=OrdedrStatus.choices ,
        default=OrdedrStatus.PENDING,
        max_length=10
    )
    product = models.ManyToManyField(Product , through="OrderItem" , related_name="orders")

    def __str__(self):
        return f"Order {self.order_id} by {self.user.username}"

# This model represents the items in an order, linking the order to the products and their quantities
class OrderItem(models.Model):
    order = models.ForeignKey(Order , on_delete=models.CASCADE , related_name="items")
    product = models.ForeignKey(Product , on_delete=models.CASCADE , related_name="products")
    quantity = models.PositiveIntegerField()

    # This property calculates the subtotal for the item based on the product price and quantity
    @property
    def item_subtotal(self):
        return self.product.price * self.quantity
    
    def __str__(self):
        return f"{self.quantity} X {self.product.name} in Order {self.order.order_id}"