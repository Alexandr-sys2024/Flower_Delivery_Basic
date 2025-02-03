from django.utils.html import format_html
from django.contrib import admin
from .models import Flower

@admin.register(Flower)
class FlowerAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'image_preview')  # Добавляем превью картинки
    fields = ('name', 'description', 'price', 'image', 'image_preview')  # Добавляем метод
    readonly_fields = ('image_preview',)  # Чтобы поле не редактировалось

    list_filter = ('created_at',)
    list_per_page = 10

    def image_preview(self, obj):
        """ Показывает превью загруженного изображения в админке """
        if obj.image:
            return format_html('<img src="{}" style="max-height: 100px;"/>', obj.image.url)
        return "(Нет изображения)"

    image_preview.short_description = "Превью"
