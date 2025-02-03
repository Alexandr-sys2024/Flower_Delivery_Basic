from django.test import TestCase
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from catalog.models import Flower

class CatalogViewsTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        """Создаём тестовые данные для всех тестов в этом классе."""
        test_image = SimpleUploadedFile(name='test_image.jpg', content=b'', content_type='image/jpeg')
        cls.flower1 = Flower.objects.create(name="Розы", description="Красивые розы", price=1500, image=test_image)
        cls.flower2 = Flower.objects.create(name="Лилии", description="Белые лилии", price=2000, image=test_image)

    def test_flower_list_view(self):
        """Тестируем отображение списка букетов."""
        response = self.client.get(reverse('flower_list'))
        self.assertEqual(response.status_code, 200)  # Ожидаем 200 OK
        self.assertTemplateUsed(response, 'catalog/flower_list.html')  # Проверяем, что используется нужный шаблон
        self.assertIn('flowers', response.context)  # Проверяем, что в контексте передаётся список букетов
        self.assertEqual(len(response.context['flowers']), 2)  # Ожидаем 2 тестовых букета

    def test_flower_detail_view(self):
        """Тест детальной страницы букета."""
        response = self.client.get(reverse('flower_detail', args=[self.flower1.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'catalog/flower_detail.html')
        self.assertEqual(response.context['flower'].name, "Розы")

    def test_flower_detail_view_404(self):
        """Тестируем 404, если букета не существует."""
        response = self.client.get(reverse('flower_detail', args=[999]))
        self.assertEqual(response.status_code, 404)

    def test_index_view(self):
        """Тестируем главную страницу, если она есть в catalog."""
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')