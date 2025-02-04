from asgiref.sync import sync_to_async
from catalog.models import Flower


@sync_to_async
def get_flower_list():
    # Получаем все букеты и возвращаем список словарей с нужными полями
    return list(Flower.objects.all().values('id', 'name', 'price'))

@sync_to_async
def get_flower_details(flower_id):
    flower = Flower.objects.get(id=flower_id)
    return {
        'id': flower.id,
        'name': flower.name,
        'price': str(flower.price),
        'description': flower.description or ""
    }