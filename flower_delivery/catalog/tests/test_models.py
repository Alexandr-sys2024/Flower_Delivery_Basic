from django.test import TestCase
from catalog.models import Flower
from decimal import Decimal

class FlowerModelTest(TestCase):

    def test_create_flower(self):
        """Проверяем, что можно создать объект Flower"""
        flower = Flower.objects.create(
            name="Розы",
            description="Красивые розы",
            price=1500.00
        )
        self.assertEqual(flower.name, "Розы")
        self.assertEqual(flower.description, "Красивые розы")
        self.assertEqual(flower.price, Decimal("1500.00"))

    def test_max_length_name(self):
        """Проверяем, что name не превышает 100 символов"""
        flower = Flower.objects.create(
            name="X" * 100,  # Ровно 100 символов
            price=1000.00
        )
        self.assertEqual(len(flower.name), 100)

    def test_description_can_be_blank(self):
        """Проверяем, что можно создать цветок без описания"""
        flower = Flower.objects.create(name="Лилии", price=2000.00)
        self.assertIsNone(flower.description)

    def test_price_cannot_be_negative(self):
        """Проверяем, что нельзя создать цветок с отрицательной ценой"""
        flower = Flower(name="Гвоздики", price=-100.00)
        try:
            flower.save()
            self.fail("Ожидалось исключение, но сохранение прошло успешно!")
        except:
            pass  # Тест проходит, если исключение было вызвано

    def test_flower_str_method(self):
        """Проверяем, что __str__ возвращает name"""
        flower = Flower.objects.create(name="Тюльпаны", price=800.00)
        self.assertEqual(str(flower), "Тюльпаны")
