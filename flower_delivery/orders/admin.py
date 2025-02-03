from django.contrib import admin
from .models import Order, OrderItem, Cart, CartItem

class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 1

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_id', 'status', 'created_at', 'updated_at')  # Заменили 'user' на 'user_id'
    list_filter = ('status', 'created_at')
    inlines = [CartItemInline]

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'cart', 'flower', 'quantity', 'price')

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_id', 'status', 'order_key', 'created_at', 'total_price')  # Исправили 'user' на 'user_id'
    list_filter = ('status', 'created_at')
    search_fields = ('order_key',)  # Убрали 'user__username', т.к. user_id — это просто число
    inlines = [OrderItemInline]

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'flower', 'quantity', 'price')