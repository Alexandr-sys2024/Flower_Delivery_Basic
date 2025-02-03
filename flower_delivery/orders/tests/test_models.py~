from django.test import TestCase
from django.contrib.auth.models import User
from orders.models import Order, OrderItem, Cart, CartItem
from catalog.models import Flower
from decimal import Decimal

class OrderModelTest(TestCase):

    def setUp(self):
        """Создаём тестового пользователя и цветок"""
        self.user = User.objects.create_user(username='testuser', password='password')
        self.flower = Flower.objects.create(name="Розы", price=1500.00)

    def test_create_order(self):
        """Проверяем создание заказа"""
        order = Order.objects.create(user=self.user, total_price=3000.00)
        self.assertEqual(order.user, self.user)
        self.assertEqual(order.total_price, Decimal('3000.00'))
        self.assertEqual(order.status, 'NEW')

    def test_order_key_generation(self):
        """Проверяем, что order_key генерируется, если не указан"""
        order = Order.objects.create(user=self.user)
        self.assertIsNotNone(order.order_key)
        self.assertEqual(len(order.order_key), 8)  # UUID[:8]

    def test_order_str_method(self):
        """Проверяем __str__ метода Order"""
        order = Order.objects.create(user=self.user)
        self.assertEqual(str(order), f"Order #{order.pk} by {self.user.username}")

class OrderItemModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.flower = Flower.objects.create(name="Розы", price=1500.00)
        self.order = Order.objects.create(user=self.user, total_price=1500.00)

    def test_create_order_item(self):
        """Проверяем создание элемента заказа"""
        order_item = OrderItem.objects.create(order=self.order, flower=self.flower, quantity=2, price=1500.00)
        self.assertEqual(order_item.order, self.order)
        self.assertEqual(order_item.flower, self.flower)
        self.assertEqual(order_item.quantity, 2)

    def test_order_item_str(self):
        """Проверяем __str__ метода OrderItem"""
        order_item = OrderItem.objects.create(order=self.order, flower=self.flower, quantity=1, price=1500.00)
        self.assertEqual(str(order_item), f"Розы x 1 (Order #{self.order.pk})")

class CartModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')

    def test_create_cart(self):
        """Проверяем создание корзины"""
        cart = Cart.objects.create(user=self.user)
        self.assertEqual(cart.user, self.user)
        self.assertEqual(cart.status, 'OPEN')

    def test_create_cart_without_user(self):
        """Проверяем, что корзина может быть без пользователя"""
        cart = Cart.objects.create(user=None)
        self.assertIsNone(cart.user)

    def test_cart_str(self):
        """Проверяем __str__ метода Cart"""
        cart = Cart.objects.create(user=self.user)
        self.assertEqual(str(cart), f"Cart #{cart.pk} - {self.user.username} (OPEN)")

class CartItemModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.flower = Flower.objects.create(name="Розы", price=1500.00)
        self.cart = Cart.objects.create(user=self.user, status='OPEN')

    def test_create_cart_item(self):
        """Проверяем создание товара в корзине"""
        cart_item = CartItem.objects.create(cart=self.cart, flower=self.flower, quantity=2, price=1500.00)
        self.assertEqual(cart_item.cart, self.cart)
        self.assertEqual(cart_item.flower, self.flower)
        self.assertEqual(cart_item.quantity, 2)

    def test_cart_item_str(self):
        """Проверяем __str__ метода CartItem"""
        cart_item = CartItem.objects.create(cart=self.cart, flower=self.flower, quantity=1, price=1500.00)
        self.assertEqual(str(cart_item), f"Розы (x1) in Cart #{self.cart.pk}")
