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

    order_id = models.UUIDField(primary_key=True ,default=uuid.uuid4)
    user = models.ForeignKey(User , on_delete=models.CASCADE , related_name="user")
    created_at = models.DateTimeField(auto_now_add=True , null=True , blank=True)
    status = models.CharField(
        choices=OrdedrStatus.choices ,
        default=OrdedrStatus.PENDING,
        max_length=10
    )
    product = models.ManyToManyField(Product , through="OrderItem" , related_name="orders")

    def __str__(self):
        return f"Order {self.order_id} by {self.user.username}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order , on_delete=models.CASCADE , related_name="items")
    product = models.ForeignKey(Product , on_delete=models.CASCADE , related_name="products")
    quantity = models.PositiveIntegerField()

    @property
    def item_subtotal(self):
        return self.product.price * self.quantitiy
    
    def __str__(self):
        return f"{self.quantitiy} X {self.product.name} in Order {self.order.order_id}"