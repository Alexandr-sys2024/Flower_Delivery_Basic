from django.shortcuts import render, get_object_or_404
from .models import Flower


def flower_list(request):
    """
    Отображает список всех букетов (товаров),
    которые будут выводиться в шаблоне 'catalog/flower_list.html'.
    """
    flowers = Flower.objects.all()
    context = {
        'flowers': flowers
    }
    return render(request, 'catalog/flower_list.html', context)


def flower_detail(request, flower_id):
    """
    (Опционально) Отображает детальную страницу
    конкретного букета/цветка.
    """
    flower = get_object_or_404(Flower, id=flower_id)
    context = {
        'flower': flower
    }
    return render(request, 'catalog/flower_detail.html', context)


def index(request):
    """
    (Опционально) Если у вас есть главная страница в приложении catalog,
    можно возвращать 'index.html' или сразу перенаправлять на 'flower_list'.
    """
    return render(request, 'index.html')


from django.shortcuts import render
from django.shortcuts import render

# Create your views here.
