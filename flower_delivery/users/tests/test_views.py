from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User

class UserViewsTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        """Создаём тестового пользователя"""
        cls.user = User.objects.create_user(username='testuser', password='password123')

    def setUp(self):
        """Создаём клиент для тестов"""
        self.client = Client()

    def test_login_success(self):
        """Проверяет, что пользователь может войти в систему"""
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'password123'
        })
        self.assertEqual(response.status_code, 302)  # Успешный вход → редирект
        self.assertRedirects(response, reverse('flower_list'))  # Перенаправление в каталог

    def test_login_invalid_password(self):
        """Проверяет, что при неверном пароле вход не выполняется"""
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 200)  # Должен остаться на той же странице
        self.assertContains(response, 'Неверное имя пользователя или пароль')

    def test_login_nonexistent_user(self):
        """Проверяет, что нельзя войти под несуществующим пользователем"""
        response = self.client.post(reverse('login'), {
            'username': 'nouser',
            'password': 'password123'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Неверное имя пользователя или пароль')

    def test_logout(self):
        """Проверяет выход пользователя"""
        self.client.login(username='testuser', password='password123')
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)  # Должен быть редирект
        self.assertRedirects(response, reverse('flower_list'))  # Перенаправление на каталог

    def test_register_success(self):
        """Проверяет успешную регистрацию нового пользователя"""
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'password1': 'newsecurepassword',
            'password2': 'newsecurepassword'
        })
        self.assertEqual(response.status_code, 302)  # Успешная регистрация → редирект
        self.assertRedirects(response, reverse('flower_list'))
        self.assertTrue(User.objects.filter(username='newuser').exists())  # Проверяем, что пользователь создан

    def test_register_password_mismatch(self):
        """Проверяет, что при несовпадении паролей регистрация не проходит"""
        response = self.client.post(reverse('register'), {
            'username': 'testuser2',
            'password1': 'password123',
            'password2': 'password456'  # Разные пароли
        })
        self.assertEqual(response.status_code, 200)  # Остаётся на странице регистрации
        self.assertContains(response, 'The two password fields didn’t match')

    def test_register_existing_user(self):
        """Проверяет, что нельзя зарегистрировать уже существующего пользователя"""
        response = self.client.post(reverse('register'), {
            'username': 'testuser',  # Уже существует
            'password1': 'password123',
            'password2': 'password123'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'A user with that username already exists')
