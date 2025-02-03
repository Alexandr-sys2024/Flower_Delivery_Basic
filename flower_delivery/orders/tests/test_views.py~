from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from catalog.models import Flower
from orders.models import Cart, CartItem, Order

class OrdersViewsTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        """Создаёт тестового пользователя и тестовые товары"""
        cls.user = User.objects.create_user(username='testuser', password='password')
        cls.flower = Flower.objects.create(name="Розы", price=1500.00)

    def setUp(self):
        """Каждый тест запускается с новым клиентом"""
        self.client = Client()

    def test_cart_view_authenticated(self):
        """Проверяет, что авторизованный пользователь может просмотреть корзину"""
        self.client.login(username='testuser', password='password')
        response = self.client.get(reverse('cart_view'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'orders/cart.html')

    def test_cart_view_redirects_for_anonymous(self):
        """Анонимный пользователь перенаправляется на страницу входа"""
        response = self.client.get(reverse('cart_view'))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith(reverse('login')))

    def test_add_to_cart_authenticated(self):
        """Тест добавления товара в корзину авторизованного пользователя"""
        self.client.login(username='testuser', password='password')
        response = self.client.get(reverse('add_to_cart', args=[self.flower.id]))
        self.assertEqual(response.status_code, 302)  # Должен быть редирект
        cart = Cart.objects.get(user=self.user)
        cart_item = CartItem.objects.filter(cart=cart, flower=self.flower).first()
        self.assertIsNotNone(cart_item)
        self.assertEqual(cart_item.quantity, 1)

    def test_add_to_cart_redirects_for_anonymous(self):
        """Анонимный пользователь не может добавить товар в корзину"""
        response = self.client.get(reverse('add_to_cart', args=[self.flower.id]))
        self.assertEqual(response.status_code, 302)  # Должен перенаправить на вход

    def test_remove_from_cart(self):
        """Тест удаления товара из корзины"""
        self.client.login(username='testuser', password='password')
        cart = Cart.objects.create(user=self.user, status='OPEN')
        CartItem.objects.create(cart=cart, flower=self.flower, quantity=2, price=self.flower.price)
        response = self.client.get(reverse('remove_from_cart', args=[self.flower.id]))
        self.assertEqual(response.status_code, 302)  # Редирект на корзину
        self.assertEqual(CartItem.objects.count(), 0)  # Проверяем, что товар удалён

    def test_checkout_creates_order(self):
        """Тест оформления заказа"""
        self.client.login(username='testuser', password='password')
        cart = Cart.objects.create(user=self.user, status='OPEN')
        CartItem.objects.create(cart=cart, flower=self.flower, quantity=2, price=self.flower.price)

        response = self.client.post(reverse('checkout'))
        self.assertEqual(response.status_code, 200)  # Ожидаем успешный рендер страницы заказа
        order = Order.objects.filter(user=self.user).first()
        self.assertIsNotNone(order)
        self.assertEqual(order.total_price, 3000)  # 2 * 1500
