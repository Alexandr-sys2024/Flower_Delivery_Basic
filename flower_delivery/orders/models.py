from django.db import models
from catalog.models import Flower
import uuid

class Order(models.Model):
    """
    Заказ теперь привязан к Telegram user_id вместо Django User.
    """
    STATUS_CHOICES = (
        ('NEW', 'Новый'),
        ('IN_PROGRESS', 'В обработке'),
        ('COMPLETED', 'Завершён'),
        ('CANCELED', 'Отменён'),
    )

    user_id = models.BigIntegerField(null=True, blank=True)  # Telegram ID пользователя
    order_key = models.CharField(max_length=50, unique=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='NEW')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.pk} for User {self.user_id}"

    def save(self, *args, **kwargs):
        if not self.order_key:
            self.order_key = str(uuid.uuid4())[:8].upper()  # Генерируем уникальный ключ
        super().save(*args, **kwargs)


class OrderItem(models.Model):
    """
    Позиция в заказе: конкретный цветок с зафиксированной ценой.
    """
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    flower = models.ForeignKey(Flower, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Фиксируем цену на момент заказа

    def __str__(self):
        return f"{self.flower.name} x {self.quantity} (Order #{self.order.pk})"


class Cart(models.Model):
    """
    Корзина теперь привязана к Telegram user_id вместо Django User.
    """
    STATUS_CHOICES = (
        ('OPEN', 'Открыта'),
        ('CHECKOUT', 'Оформлена'),
        ('COMPLETED', 'Завершена'),
        ('CANCELED', 'Отменена'),
    )

    user_id = models.BigIntegerField(null=True, blank=True, unique=False)  # Telegram ID вместо ForeignKey
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='OPEN')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Cart #{self.pk} - User {self.user_id} ({self.status})"


class CartItem(models.Model):
    """
    Позиция в корзине. Фиксируем цену товара при добавлении.
    """
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    flower = models.ForeignKey(Flower, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Фиксируем цену на момент добавления

    def save(self, *args, **kwargs):
        """При добавлении фиксируем текущую цену цветка"""
        if not self.price:
            self.price = self.flower.price
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.flower.name} (x{self.quantity}) in Cart #{self.cart.pk}"
