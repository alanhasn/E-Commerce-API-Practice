from django.contrib import admin

from .models import Order, OrderItem, User


class OrderItemInline(admin.TabularInline):
    model = OrderItem

class OrderAdmin(admin.ModelAdmin):
    inlines = [
        OrderItemInline
    ]

admin.site.register(Order , OrderAdmin)
admin.site.register(User)