from django.test import TestCase
from django.contrib.auth.models import User

class UserTests(TestCase):
    def test_user_registration(self):
        """Проверка создания пользователя"""
        user = User.objects.create_user(username="newuser", password="password")
        self.assertTrue(User.objects.filter(username="newuser").exists())
